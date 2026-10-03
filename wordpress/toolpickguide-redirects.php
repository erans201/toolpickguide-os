<?php
/**
 * Plugin Name: ToolPickGuide Redirects
 * Description: Permanent (301) redirects for retired duplicate posts. Used when Hostinger's firewall blocks creating redirects in Rank Math. Exact path match only; query strings are carried over.
 * Version: 1.0
 *
 * Install: upload to wp-content/mu-plugins/ (same folder as the auth bridge). Loads automatically.
 * Add a redirect: add a line to $tpg_redirects below ('/old-path/' => '/new-path/'), then re-upload.
 * Remove: delete the file.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action(
	'template_redirect',
	function () {
		$tpg_redirects = array(
			'/best-crm-for-coaches/'                          => '/client-management-software-for-coaches/',
			'/best-accounting-practice-management-software/' => '/best-practice-management-accountants/',
		);

		$path = isset( $_SERVER['REQUEST_URI'] ) ? (string) wp_parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH ) : '';
		$path = '/' . trim( $path, '/' ) . '/';

		if ( isset( $tpg_redirects[ $path ] ) ) {
			$query  = isset( $_SERVER['QUERY_STRING'] ) && '' !== $_SERVER['QUERY_STRING'] ? '?' . $_SERVER['QUERY_STRING'] : '';
			$target = home_url( $tpg_redirects[ $path ] ) . $query;
			wp_safe_redirect( $target, 301, 'ToolPickGuide' );
			exit;
		}
	},
	1
);
