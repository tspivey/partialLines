import globalPluginHandler
import api
import textInfos
import speech
import scriptHandler
import controlTypes
import addonHandler
addonHandler.initTranslation()
from editableText import EditableText, isScriptWaiting, willSayAllResume
import config
import ui
import review
import braille

mode = 'full'

def _caretScriptPostMovedHelper(self, speakUnit, gesture, info=None):
	if isScriptWaiting():
		return
	if not info:
		try:
			info = self.makeTextInfo(textInfos.POSITION_CARET)
		except:
			return
	review.handleCaretMove(info)
	if speakUnit and not willSayAllResume(gesture):
		info2 = info.copy()
		info.expand(speakUnit)
		if speakUnit == textInfos.UNIT_LINE and mode == 'start':
			info.setEndPoint(info2, "endToEnd")
		elif speakUnit == textInfos.UNIT_LINE and mode == 'end':
			info.setEndPoint(info2, "startToStart")
		speech.speakTextInfo(info, unit=speakUnit, reason=controlTypes.REASON_CARET)
	braille.handler.handleCaretMove(self)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self):
		super(GlobalPlugin, self).__init__()
		global old
		old = EditableText._caretScriptPostMovedHelper
		EditableText._caretScriptPostMovedHelper = _caretScriptPostMovedHelper

	def script_reportToStartOfLine(self,gesture):
		obj=api.getFocusObject()
		treeInterceptor=obj.treeInterceptor
		if hasattr(treeInterceptor,'TextInfo') and not treeInterceptor.passThrough:
			obj=treeInterceptor
		try:
			info=obj.makeTextInfo(textInfos.POSITION_CARET)
			info2 = info.copy()
		except (NotImplementedError, RuntimeError):
			info=obj.makeTextInfo(textInfos.POSITION_FIRST)
			info2 = info.copy()
		info.expand(textInfos.UNIT_LINE)
		info.setEndPoint(info2, "endToEnd")
		if scriptHandler.getLastScriptRepeatCount()==0:
			speech.speakTextInfo(info,unit=textInfos.UNIT_LINE,reason=controlTypes.REASON_CARET)
		else:
			speech.speakSpelling(info.text)
	script_reportToStartOfLine.__doc__ = _("Read from cursor to start of line")

	def script_reportToEndOfLine(self,gesture):
		obj=api.getFocusObject()
		treeInterceptor=obj.treeInterceptor
		if hasattr(treeInterceptor,'TextInfo') and not treeInterceptor.passThrough:
			obj=treeInterceptor
		try:
			info=obj.makeTextInfo(textInfos.POSITION_CARET)
			info2 = info.copy()
		except (NotImplementedError, RuntimeError):
			info=obj.makeTextInfo(textInfos.POSITION_FIRST)
			info2 = info.copy()
		info.expand(textInfos.UNIT_LINE)
		info.setEndPoint(info2, "startToStart")
		if scriptHandler.getLastScriptRepeatCount()==0:
			speech.speakTextInfo(info,unit=textInfos.UNIT_LINE,reason=controlTypes.REASON_CARET)
		else:
			speech.speakSpelling(info.text)
	script_reportToEndOfLine.__doc__ = _("Read from cursor to end of line")

	def script_setLineReadingMode(self, gesture):
		global mode
		if mode == 'full':
			mode = 'start'
			ui.message(_("Read to start"))
		elif mode == 'start':
			mode = 'end'
			ui.message(_("Read to end"))
		elif mode == 'end':
			mode = 'full'
			ui.message(_("Read entire line"))
	script_setLineReadingMode.__doc__ = _("When using the arrow keys, toggle line reading mode between read to start, read to end, and read complete line.")

	def terminate(self):
		EditableText._caretScriptPostMovedHelper = old

	__gestures = {
	"kb:NVDA+shift+pageUp":"reportToStartOfLine",
	"kb:NVDA+shift+pageDown":"reportToEndOfLine",
	"kb:NVDA+shift+delete": "setLineReadingMode",
}
