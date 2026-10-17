<?php
/**
 * Plugin Name: ToolPickGuide Photo Credits
 * Description: Pexels API guidelines (user decision 2026-10-17): a site-wide "Photos provided by Pexels" link in the footer, and a small "Photos:" credit line under each post listing the photographers of the Pexels images it uses (read from the Media Library captions that stock_photo.py / upload_draft.py set).
 * Version: 1.0
 *
 * Install: upload to wp-content/mu-plugins/. Must-use plugins load automatically.
 * Remove: delete the file.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( 'post' ) || ! in_the_loop() || ! is_main_query() ) {
		return $content;
	}
	$ids = array();
	$featured = get_post_thumbnail_id();
	if ( $featured ) {
		$ids[] = (int) $featured;
	}
	if ( preg_match_all( '/wp-image-(\d+)/', $content, $m ) ) {
		$ids = array_merge( $ids, array_map( 'intval', $m[1] ) );
	}
	$credits = array();
	foreach ( array_unique( $ids ) as $id ) {
		$caption = wp_get_attachment_caption( $id );
		if ( $caption && false !== stripos( $caption, 'Pexels' ) ) {
			$credits[] = wp_kses( $caption, array( 'a' => array( 'href' => array(), 'rel' => array() ) ) );
		}
	}
	if ( ! $credits ) {
		return $content;
	}
	return $content . '<p class="tpg-photo-credits" style="font-size:.85em;opacity:.8">Photos: ' . implode( ' · ', array_unique( $credits ) ) . '</p>';
}, 20 );

add_action( 'wp_footer', function () {
	echo '<p class="tpg-pexels-link" style="text-align:center;font-size:.8em;opacity:.7;margin:8px 0">'
		. '<a href="https://www.pexels.com" rel="noopener" target="_blank">Photos provided by Pexels</a></p>';
} );
