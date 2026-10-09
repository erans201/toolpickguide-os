<?php
/**
 * Plugin Name: ToolPickGuide Clarity
 * Description: Adds the Microsoft Clarity tag (heatmaps, scroll depth, session recordings) to every public page. Logged-in users (the owner and editors) are not tracked, so our own visits don't distort the data. User decision 2026-10-09: judge articles by user behavior too (knowledge/content-test.md).
 * Version: 1.0
 *
 * Install: put the Clarity project ID below (Clarity → Settings → Overview → Project ID; it is public, not a secret),
 * then upload to wp-content/mu-plugins/. Must-use plugins load automatically.
 * Remove: delete the file.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'TPG_CLARITY_PROJECT_ID', 'PUT-PROJECT-ID-HERE' );

add_action( 'wp_head', function () {
	if ( is_user_logged_in() || is_admin() || ! preg_match( '/^[a-z0-9]{6,20}$/', TPG_CLARITY_PROJECT_ID ) ) {
		return;
	}
	?>
<script type="text/javascript">
(function(c,l,a,r,i,t,y){
c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
})(window, document, "clarity", "script", "<?php echo esc_js( TPG_CLARITY_PROJECT_ID ); ?>");
</script>
	<?php
}, 20 );
