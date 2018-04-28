"""
Figure Tag
----------
This implements a Liquid-style figure tag for Pelican,
based on the image tag.

Syntax
------
{% figure [img class name(s)] [http[s]:/]/path/to/image [width [height]] [caption] %}

Examples
--------
{% figure /images/ninja.png Ninja Attack! %}
{% figure left half http://site.com/images/ninja.png Ninja Attack! %}
{% figure left half http://site.com/images/ninja.png 150 150 Ninja Attack! %}

Output
------
<figure><img src="/images/ninja.png" alt="Ninja Attack!"><figcaption>Ninja Attack!</figcaption></figure>
<figure><img class="left half" src="http://site.com/images/ninja.png" alt="Ninja Attack!"><figcaption>Ninja Attack!</figcaption></figure>
<figure><img class="left half" src="http://site.com/images/ninja.png" width="150" height="150" alt="Ninja Attack!"><figcaption>Ninja Attack!</figcaption></figure>
"""
import re
from .mdx_liquid_tags import LiquidTags
import six

SYNTAX = '{% figure [class name(s)] [http[s]:/]/path/to/image [width [height]] [figure caption | "figure caption" ["alt text"]] %}'

# Regular expression to match the entire syntax
ReImg = re.compile("""(?P<class>\S.*\s+)?(?P<src>(?:https?:\/\/|\/|\S+\/)\S+)(?:\s+(?P<width>\d+))?(?:\s+(?P<height>\d+))?(?P<caption>\s+.+)?""")

@LiquidTags.register('figure')
def figure(preprocessor, tag, markup):
    attrs = None
    caption_attrs = None

    # Parse the markup string
    match = ReImg.search(markup)
    if match:
        attrs = dict([(key, val.strip())
                      for (key, val) in six.iteritems(match.groupdict()) if val])
    else:
        raise ValueError('Error processing input. '
                         'Expected syntax: {0}'.format(SYNTAX))

    # Check if caption text is present -- if so, split it from title
    if 'caption' in attrs:
        caption_attrs = {}    
        caption_attrs['caption'] = attrs.pop('caption')    
        attrs['alt'] = caption_attrs['caption']
                
    # Return the formatted text
    img_tag = "<img {0}>".format(' '.join('{0}="{1}"'.format(key, val)
                                       for (key, val) in six.iteritems(attrs)))
    if caption_attrs:
        figcaption_tag = '<figcaption>{}</figcaption>'.format(caption_attrs['caption'])
        return "<figure>{}{}</figure>".format(img_tag, figcaption_tag)
    else:
        return "<figure>{}</figure>".format(img_tag)

#----------------------------------------------------------------------
# This import allows image tag to be a Pelican plugin
from .liquid_tags import register

