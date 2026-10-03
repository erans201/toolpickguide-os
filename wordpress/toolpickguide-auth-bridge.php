<?php
/**
 * Plugin Name: ToolPickGuide REST Auth Bridge
 * Description: Hostinger's edge (hcdn) strips the Authorization header before WordPress sees it, which breaks application passwords. This copies the X-WP-Auth header sent by upload_draft.py into the fields WordPress reads, and makes sure WordPress treats /wp-json/ requests as API requests even if another plugin checks the current user early. WordPress still validates the application password normally; this grants no access by itself.
 * Version: 1.1
 *
 * Install: upload this file to wp-content/mu-plugins/ (replace the old copy).
 * Must-use plugins load automatically. There is nothing to activate.
 * Remove: delete the file.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// Diagnostic state, reported in the X-TPG-Bridge response header (no credentials, no user data).
$GLOBALS['tpg_bridge_state'] = 'no-fallback-header';

$tpg_https = ( ! empty( $_SERVER['HTTPS'] ) && 'off' !== strtolower( $_SERVER['HTTPS'] ) )
	|| ( isset( $_SERVER['HTTP_X_FORWARDED_PROTO'] ) && 'https' === strtolower( $_SERVER['HTTP_X_FORWARDED_PROTO'] ) );

if ( ! empty( $_SERVER['PHP_AUTH_USER'] ) || ! empty( $_SERVER['HTTP_AUTHORIZATION'] ) ) {
	$GLOBALS['tpg_bridge_state'] = 'native-header-present';
} elseif ( ! empty( $_SERVER['HTTP_X_WP_AUTH'] ) ) {
	$GLOBALS['tpg_bridge_state'] = $tpg_https ? 'fallback-header-invalid' : 'fallback-header-not-https';

	if ( $tpg_https ) {
		$tpg_header = trim( wp_unslash( $_SERVER['HTTP_X_WP_AUTH'] ) );

		if ( 0 === stripos( $tpg_header, 'Basic ' ) ) {
			$tpg_decoded = base64_decode( substr( $tpg_header, 6 ), true );

			if ( false !== $tpg_decoded && false !== strpos( $tpg_decoded, ':' ) ) {
				list( $tpg_user, $tpg_pass ) = explode( ':', $tpg_decoded, 2 );
				$_SERVER['HTTP_AUTHORIZATION'] = $tpg_header;
				$_SERVER['PHP_AUTH_USER']      = $tpg_user;
				$_SERVER['PHP_AUTH_PW']        = $tpg_pass;
				$GLOBALS['tpg_bridge_state']   = 'applied';
			}
		}

		unset( $tpg_header, $tpg_decoded, $tpg_user, $tpg_pass );
	}
}

unset( $tpg_https );

/**
 * WordPress only accepts application passwords once REST_REQUEST is defined. If a plugin
 * (e.g., a cache plugin) resolves the current user before that, the password is silently
 * ignored. Treat /wp-json/ and ?rest_route= requests as API requests from the start.
 */
add_filter(
	'application_password_is_api_request',
	function ( $is_api_request ) {
		if ( $is_api_request ) {
			return true;
		}
		$uri    = isset( $_SERVER['REQUEST_URI'] ) ? (string) $_SERVER['REQUEST_URI'] : '';
		$prefix = '/' . trim( rest_get_url_prefix(), '/' ) . '/';
		return false !== strpos( $uri, $prefix ) || isset( $_GET['rest_route'] );
	}
);

// Diagnostic header on REST responses. Remove this block once uploads work.
add_filter(
	'rest_post_dispatch',
	function ( $response ) {
		if ( $response instanceof WP_HTTP_Response ) {
			$response->header( 'X-TPG-Bridge', $GLOBALS['tpg_bridge_state'] . '; v1.1' );
		}
		return $response;
	}
);
