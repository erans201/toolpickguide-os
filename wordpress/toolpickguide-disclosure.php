<?php
/**
 * Plugin Name: ToolPickGuide Affiliate Disclosure
 * Description: Adds the standard affiliate disclosure (with the FTC link) at the top of any post that contains an affiliate link (rel="sponsored") but no disclosure of its own. Keeps every page with affiliate links FTC-compliant, including Junia articles and links the robots add later.
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
	if ( false === stripos( $content, 'sponsored' ) ) {
		return $content; // no affiliate link on this page
	}
	if ( false !== stripos( $content, 'Affiliate disclosure' ) || false !== stripos( $content, 'may earn ToolPickGuide' )
		|| false !== stripos( $content, 'Disclosure:' ) ) {
		return $content; // the article already discloses
	}
	$box = '<p class="tpg-disclosure"><strong>Affiliate disclosure:</strong> Some links here may earn ToolPickGuide a commission. '
		. 'It never changes the order. If a tool is wrong for you, we&#8217;ll say so. Why we disclose: the '
		. '<a href="https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking" rel="noopener" target="_blank">'
		. 'FTC&#8217;s endorsement guidance</a>.</p>';
	return $box . $content;
}, 5 );
