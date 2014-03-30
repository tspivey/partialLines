# Build customizations
# Change this file instead of sconstruct or manifest files, whenever possible.

# Full getext (please don't change)
_ = lambda x : x

# Add-on information variables
addon_info = {
	# add-on Name
	"addon-name" : "partial-lines",
	# Add-on description
	# TRANSLATORS: Summary for this add-on to be shown on installation and add-on information.
	"addon-summary" : _("Read partial lines"),
	# Add-on description
	# Translators: Long description to be shown for this add-on on installation and add-on information
	"addon-description" : _("Read partial lines. NVDA+shift+page up reads to the start of current line, NVDA+shift+page down reads to the end. NVDA+shift+delete toggles what happens when you press the up/down arrow keys between read entire line, read to start and read to end."),
	# version
	"addon-version" : "0.20140329.01",
	# Author(s)
	"addon-author" : "Tyler Spivey <tspivey@pcdesk.net>",
	# URL for the add-on documentation support
	"addon-url" : None
}


import os.path

# Define the python files that are the sources of your add-on.
# You can use glob expressions here, they will be expanded.
pythonSources = ['addon/globalPlugins/line.py']

# Files that contain strings for translation. Usually your python sources
i18nSources = pythonSources + ["buildVars.py"]

# Files that will be ignored when building the nvda-addon file
# Paths are relative to the addon directory, not to the root directory of your addon sources.
excludedFiles = []
