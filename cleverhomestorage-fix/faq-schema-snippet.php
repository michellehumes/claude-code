<?php
/**
 * FAQ Schema JSON-LD for CleverHomeStorage.com
 * Add this to your theme's functions.php or use a Code Snippets plugin.
 *
 * This automatically detects FAQ sections in posts (looking for
 * common FAQ heading patterns and Q&A structures) and outputs
 * FAQPage schema markup.
 */
add_action('wp_footer', 'chs_faq_schema_output');

function chs_faq_schema_output() {
    if (!is_singular('post')) {
        return;
    }

    global $post;
    $content = $post->post_content;

    // Look for FAQ section - check if the post has FAQ-related headings
    if (
        stripos($content, 'frequently asked') === false &&
        stripos($content, 'FAQ') === false &&
        stripos($content, 'common questions') === false
    ) {
        return;
    }

    // Extract Q&A pairs from heading + paragraph patterns
    // Matches h2/h3/h4 headings followed by content (common WordPress FAQ structure)
    $faqs = array();

    // Pattern: WordPress block or classic editor headings with question marks
    if (preg_match_all(
        '/<h[2-4][^>]*>(.*?\?)<\/h[2-4]>\s*(?:<p[^>]*>)?(.*?)(?:<\/p>|<h[2-4])/si',
        $content,
        $matches,
        PREG_SET_ORDER
    )) {
        foreach ($matches as $match) {
            $question = wp_strip_all_tags(trim($match[1]));
            $answer = wp_strip_all_tags(trim($match[2]));
            if (!empty($question) && !empty($answer)) {
                $faqs[] = array(
                    '@type' => 'Question',
                    'name' => $question,
                    'acceptedAnswer' => array(
                        '@type' => 'Answer',
                        'text' => $answer,
                    ),
                );
            }
        }
    }

    if (empty($faqs)) {
        return;
    }

    $schema = array(
        '@context' => 'https://schema.org',
        '@type' => 'FAQPage',
        'mainEntity' => $faqs,
    );

    echo '<script type="application/ld+json">' . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . '</script>' . "\n";
}
