import globalPluginHandler
import api
import textInfos
import speech
import scriptHandler
import controlTypes

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
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

	__gestures = {
	"kb:NVDA+shift+pageUp":"reportToStartOfLine",
	"kb:NVDA+shift+pageDown":"reportToEndOfLine",
}
