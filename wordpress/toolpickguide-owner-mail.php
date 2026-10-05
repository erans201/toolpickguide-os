<?php
/**
 * Plugin Name: ToolPickGuide Owner Mail
 * Description: Lets the ToolPickGuide robot email its run update to the site owner. The cloud robot can't open a mail connection itself, so it posts the message here over HTTPS and WordPress sends it with wp_mail(). The recipient is fixed below; the endpoint cannot email anyone else. Requires a logged-in user who can edit posts (the robot's application password), and is capped at 10 emails a day.
 * Version: 1.0
 *
 * Install: upload this file to wp-content/mu-plugins/ (next to toolpickguide-auth-bridge.php).
 * Must-use plugins load automatically. There is nothing to activate.
 * Remove: delete the file.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const TPG_OWNER_MAIL_TO   = 'cezaris.joe@gmail.com'; // the only recipient (user decision 2026-10-05)
const TPG_OWNER_MAIL_FROM = 'eran@toolpickguide.com';
const TPG_OWNER_MAIL_CAP  = 10; // emails per day

add_action(
	'rest_api_init',
	function () {
		register_rest_route(
			'tpg/v1',
			'/notify-owner',
			array(
				'methods'             => 'POST',
				'permission_callback' => function () {
					return current_user_can( 'edit_posts' );
				},
				'args'                => array(
					'subject' => array(
						'required' => true,
						'type'     => 'string',
					),
					'body'    => array(
						'required' => true,
						'type'     => 'string',
					),
				),
				'callback'            => 'tpg_owner_mail_send',
			)
		);
	}
);

function tpg_owner_mail_send( WP_REST_Request $request ) {
	$key   = 'tpg_owner_mail_' . gmdate( 'Ymd' );
	$count = (int) get_transient( $key );
	if ( $count >= TPG_OWNER_MAIL_CAP ) {
		return new WP_Error( 'tpg_cap', 'Daily email cap reached.', array( 'status' => 429 ) );
	}

	$subject = substr( sanitize_text_field( $request->get_param( 'subject' ) ), 0, 200 );
	$body    = substr( sanitize_textarea_field( $request->get_param( 'body' ) ), 0, 20000 );
	if ( '' === trim( $body ) ) {
		return new WP_Error( 'tpg_empty', 'Empty message.', array( 'status' => 400 ) );
	}

	$headers = array(
		'Content-Type: text/plain; charset=UTF-8',
		'From: ToolPickGuide robot <' . TPG_OWNER_MAIL_FROM . '>',
	);
	$sent    = wp_mail( TPG_OWNER_MAIL_TO, $subject, $body, $headers );

	set_transient( $key, $count + 1, DAY_IN_SECONDS );
	if ( ! $sent ) {
		return new WP_Error( 'tpg_not_sent', 'wp_mail() could not send.', array( 'status' => 500 ) );
	}
	return array(
		'sent' => true,
		'to'   => TPG_OWNER_MAIL_TO,
	);
}
