<?php
/**
 * Plugin Name: ToolPickGuide Archive Titles
 * Description: Removes the "Category:" / "Tag:" prefix WordPress adds to archive headings, so category pages show "Reviews" instead of "Category Reviews".
 * Version: 1.0
 *
 * Install: upload to wp-content/mu-plugins/. Must-use plugins load automatically.
 * Remove: delete the file.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_filter( 'get_the_archive_title_prefix', '__return_empty_string' );
