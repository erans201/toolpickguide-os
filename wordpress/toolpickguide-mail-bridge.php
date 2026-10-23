<?php
/**
 * Plugin Name: ToolPickGuide Mail Bridge
 * Description: Lets the ToolPickGuide cloud robot read affiliate-program emails and reply to them (owner decision 2026-10-23: "OK full email"). The cloud can't open mail connections itself, so WordPress does it over HTTPS: it reads the business mailbox READ-ONLY and returns only emails from the sender domains the robot asks for (knowledge/affiliate-senders.txt), and it sends a reply only to an address that has emailed us in the last 90 days. Max 5 replies a day; a copy of each reply goes to the Sent folder. Requires a logged-in user who can edit posts (the robot's application password).
 * Version: 1.0
 *
 * Install: 1) upload this file to wp-content/mu-plugins/ (next to toolpickguide-owner-mail.php);
 *          2) in wp-config.php, above the line "That's all, stop editing!", add the mailbox login:
 *               define( 'TPG_MAIL_USER', 'eran@toolpickguide.com' );
 *               define( 'TPG_MAIL_PASS', 'the mailbox password' );
 * Must-use plugins load automatically. Remove: delete the file (and the two lines).
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const TPG_MAIL_IMAP      = 'ssl://imap.hostinger.com:993';
const TPG_MAIL_REPLY_CAP = 5;   // replies per day
const TPG_MAIL_SCAN_MAX  = 300; // newest messages looked at per inbox call

add_action(
	'rest_api_init',
	function () {
		$can = function () {
			return current_user_can( 'edit_posts' );
		};
		register_rest_route( 'tpg/v1', '/mail/inbox', array( 'methods' => 'POST', 'permission_callback' => $can, 'callback' => 'tpg_mail_inbox' ) );
		register_rest_route( 'tpg/v1', '/mail/reply', array( 'methods' => 'POST', 'permission_callback' => $can, 'callback' => 'tpg_mail_reply' ) );
	}
);

/* ---------- minimal IMAP client (read-only use + APPEND to Sent) ---------- */

function tpg_imap_open() {
	if ( ! defined( 'TPG_MAIL_USER' ) || ! defined( 'TPG_MAIL_PASS' ) ) {
		return new WP_Error( 'tpg_mail_config', 'TPG_MAIL_USER / TPG_MAIL_PASS are not set in wp-config.php.', array( 'status' => 500 ) );
	}
	$fp = @stream_socket_client( TPG_MAIL_IMAP, $errno, $errstr, 20 );
	if ( ! $fp ) {
		return new WP_Error( 'tpg_mail_connect', 'IMAP connection failed: ' . $errstr, array( 'status' => 502 ) );
	}
	stream_set_timeout( $fp, 30 );
	fgets( $fp ); // greeting
	$q   = function ( $s ) {
		return '"' . addcslashes( $s, '"\\' ) . '"';
	};
	$res = tpg_imap_cmd( $fp, 'LOGIN ' . $q( TPG_MAIL_USER ) . ' ' . $q( TPG_MAIL_PASS ) );
	if ( ! $res['ok'] ) {
		fclose( $fp );
		return new WP_Error( 'tpg_mail_login', 'IMAP login failed.', array( 'status' => 502 ) );
	}
	return $fp;
}

/** Sends one command; returns ['ok' => bool, 'lines' => untagged lines, 'literals' => literal blocks in order]. */
function tpg_imap_cmd( $fp, $cmd ) {
	static $n = 0;
	$tag = 'T' . ( ++$n );
	fwrite( $fp, "$tag $cmd\r\n" );
	$lines    = array();
	$literals = array();
	while ( ( $line = fgets( $fp ) ) !== false ) {
		if ( preg_match( '/\{(\d+)\}\r\n$/', $line, $m ) ) {
			$left = (int) $m[1];
			$data = '';
			while ( $left > 0 && ! feof( $fp ) ) {
				$chunk = fread( $fp, min( 8192, $left ) );
				if ( false === $chunk || '' === $chunk ) {
					break;
				}
				$data .= $chunk;
				$left -= strlen( $chunk );
			}
			$literals[] = $data;
			$lines[]    = $line;
			continue;
		}
		if ( 0 === strpos( $line, "$tag " ) ) {
			return array( 'ok' => (bool) preg_match( "/^$tag OK/", $line ), 'lines' => $lines, 'literals' => $literals );
		}
		$lines[] = $line;
	}
	return array( 'ok' => false, 'lines' => $lines, 'literals' => $literals );
}

function tpg_imap_close( $fp ) {
	tpg_imap_cmd( $fp, 'LOGOUT' );
	fclose( $fp );
}

function tpg_mail_domain_ok( $addr, $domains ) {
	$addr = strtolower( trim( $addr ) );
	$dom  = substr( (string) strrchr( $addr, '@' ), 1 );
	foreach ( $domains as $d ) {
		$d = strtolower( trim( $d ) );
		if ( $d && $dom && ( $dom === $d || substr( $dom, -strlen( ".$d" ) ) === ".$d" ) ) {
			return true;
		}
	}
	return false;
}

function tpg_mail_from_addr( $header ) {
	if ( preg_match( '/<([^>\s]+@[^>\s]+)>/', $header, $m ) ) {
		return $m[1];
	}
	return preg_match( '/[\w.+-]+@[\w.-]+/', $header, $m ) ? $m[0] : '';
}

/* ---------- endpoints ---------- */

/** POST {days, domains[]} → messages (raw RFC822, base64) from those sender domains only. Read-only (EXAMINE + BODY.PEEK). */
function tpg_mail_inbox( WP_REST_Request $request ) {
	$days    = (int) $request->get_param( 'days' );
	$days    = max( 1, min( 90, $days ? $days : 30 ) );
	$domains = array_filter( array_map( 'sanitize_text_field', (array) $request->get_param( 'domains' ) ) );
	if ( ! $domains ) {
		return new WP_Error( 'tpg_mail_domains', 'Send the allowed sender domains.', array( 'status' => 400 ) );
	}
	$fp = tpg_imap_open();
	if ( is_wp_error( $fp ) ) {
		return $fp;
	}
	tpg_imap_cmd( $fp, 'EXAMINE INBOX' );
	$since = gmdate( 'd-M-Y', time() - $days * DAY_IN_SECONDS );
	$res   = tpg_imap_cmd( $fp, "UID SEARCH SINCE $since" );
	$uids  = array();
	foreach ( $res['lines'] as $l ) {
		if ( 0 === strpos( $l, '* SEARCH' ) ) {
			$uids = array_filter( array_map( 'intval', preg_split( '/\s+/', trim( substr( $l, 8 ) ) ) ) );
		}
	}
	$uids   = array_slice( array_reverse( $uids ), 0, TPG_MAIL_SCAN_MAX );
	$out    = array();
	$hidden = 0;
	foreach ( $uids as $uid ) {
		$h    = tpg_imap_cmd( $fp, "UID FETCH $uid (BODY.PEEK[HEADER.FIELDS (FROM)])" );
		$from = tpg_mail_from_addr( implode( '', $h['literals'] ) );
		if ( ! tpg_mail_domain_ok( $from, $domains ) ) {
			++$hidden;
			continue;
		}
		$b     = tpg_imap_cmd( $fp, "UID FETCH $uid (BODY.PEEK[])" );
		$out[] = array( 'uid' => $uid, 'raw' => base64_encode( substr( implode( '', $b['literals'] ), 0, 400000 ) ) );
		if ( count( $out ) >= 40 ) {
			break;
		}
	}
	tpg_imap_close( $fp );
	return array( 'messages' => $out, 'hidden' => $hidden, 'days' => $days );
}

/** POST {to, subject, body, in_reply_to?} → sends a plain-text reply; only to an address that emailed us in the last 90 days. */
function tpg_mail_reply( WP_REST_Request $request ) {
	$to      = sanitize_email( $request->get_param( 'to' ) );
	$subject = substr( sanitize_text_field( $request->get_param( 'subject' ) ), 0, 200 );
	$body    = substr( sanitize_textarea_field( $request->get_param( 'body' ) ), 0, 20000 );
	$irt     = preg_replace( '/[^\w.@<>$%+=-]/', '', (string) $request->get_param( 'in_reply_to' ) );
	if ( ! is_email( $to ) || '' === $subject || '' === trim( $body ) ) {
		return new WP_Error( 'tpg_mail_bad', 'Need one valid To address, a subject and a body.', array( 'status' => 400 ) );
	}
	$key   = 'tpg_mail_reply_' . gmdate( 'Ymd' );
	$count = (int) get_transient( $key );
	if ( $count >= TPG_MAIL_REPLY_CAP ) {
		return new WP_Error( 'tpg_cap', 'Daily reply cap reached.', array( 'status' => 429 ) );
	}
	$fp = tpg_imap_open();
	if ( is_wp_error( $fp ) ) {
		return $fp;
	}
	tpg_imap_cmd( $fp, 'EXAMINE INBOX' );
	$since = gmdate( 'd-M-Y', time() - 90 * DAY_IN_SECONDS );
	$res   = tpg_imap_cmd( $fp, 'UID SEARCH SINCE ' . $since . ' FROM "' . addcslashes( $to, '"\\' ) . '"' );
	$found = false;
	foreach ( $res['lines'] as $l ) {
		if ( 0 === strpos( $l, '* SEARCH' ) && '' !== trim( substr( $l, 8 ) ) ) {
			$found = true;
		}
	}
	if ( ! $found ) {
		tpg_imap_close( $fp );
		return new WP_Error( 'tpg_mail_not_reply', "Refused: $to has not emailed us in the last 90 days (replies only).", array( 'status' => 403 ) );
	}
	$headers = array( 'Content-Type: text/plain; charset=UTF-8', 'From: Eran Shalev <' . TPG_MAIL_USER . '>' );
	if ( $irt ) {
		$headers[] = "In-Reply-To: $irt";
		$headers[] = "References: $irt";
	}
	$sent = wp_mail( $to, $subject, $body, $headers );
	set_transient( $key, $count + 1, DAY_IN_SECONDS );
	if ( ! $sent ) {
		tpg_imap_close( $fp );
		return new WP_Error( 'tpg_not_sent', 'wp_mail() could not send.', array( 'status' => 500 ) );
	}
	// Copy to the Sent folder so the owner sees the reply in webmail.
	$msg  = 'From: Eran Shalev <' . TPG_MAIL_USER . ">\r\nTo: $to\r\nSubject: =?UTF-8?B?" . base64_encode( $subject ) . "?=\r\n";
	$msg .= 'Date: ' . gmdate( 'D, d M Y H:i:s' ) . " +0000\r\n" . ( $irt ? "In-Reply-To: $irt\r\n" : '' );
	$msg .= "MIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n\r\n";
	$msg .= str_replace( "\n", "\r\n", str_replace( "\r\n", "\n", $body ) ) . "\r\n";
	$copied = false;
	foreach ( array( 'INBOX.Sent', 'Sent' ) as $folder ) {
		fwrite( $fp, "A1 APPEND \"$folder\" (\\Seen) {" . strlen( $msg ) . "}\r\n" );
		$cont = (string) fgets( $fp );
		if ( 0 !== strpos( $cont, '+' ) ) {
			continue;
		}
		fwrite( $fp, $msg . "\r\n" );
		while ( ( $line = fgets( $fp ) ) !== false ) {
			if ( 0 === strpos( $line, 'A1 ' ) ) {
				$copied = (bool) preg_match( '/^A1 OK/', $line );
				break;
			}
		}
		if ( $copied ) {
			break;
		}
	}
	tpg_imap_close( $fp );
	return array( 'sent' => true, 'to' => $to, 'copied_to_sent' => $copied, 'replies_today' => $count + 1 );
}
