import json

from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.operate.base_extra import BaseExtra
from ultipa.structs import Graph
from ultipa.types import ULTIPA, ULTIPA_RESPONSE
from ultipa.utils import UQLMAKER, CommandList
from ultipa.utils.ResposeFormat import ResponseKeyFormat

REPLACE_KEYS = {
	"graph": "name",
}


class GraphExtra(BaseExtra):

	def listGraph(self, requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseGraph:
		return self.showGraph(requestConfig)

	def showGraph(self, requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseGraph:
		uqlMaker = UQLMAKER(command=CommandList.showGraph, commonParams=requestConfig)
		uqlMaker.setCommandParams("")
		res = self.UqlListSimple(uqlMaker=uqlMaker, responseKeyFormat=ResponseKeyFormat(keyReplace=REPLACE_KEYS))
		return res

	def getGraph(self, graphName: str, requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		uqlMaker = UQLMAKER(command=CommandList.showGraph, commonParams=requestConfig)
		uqlMaker.setCommandParams(graphName)

		res = self.UqlListSimple(uqlMaker=uqlMaker, responseKeyFormat=ResponseKeyFormat(keyReplace=REPLACE_KEYS))
		return res

	def createGraph(self, grpah: Graph,
					requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		uqlMaker = UQLMAKER(command=CommandList.createGraph, commonParams=requestConfig)
		if grpah.description:
			uqlMaker.setCommandParams([grpah.graph, grpah.description])
		else:
			uqlMaker.setCommandParams(grpah.graph)
		res = self.uqlSingle(uqlMaker)
		return res

	def dropGraph(self, graphName: str,
				  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		uqlMaker = UQLMAKER(command=CommandList.dropGraph, commonParams=requestConfig)
		uqlMaker.setCommandParams(graphName)
		res = self.uqlSingle(uqlMaker)
		return res

	def alterGraph(self, oldGraphName: str, newGraphName: str, newDescription: str=None,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		requestConfig.graphName = oldGraphName
		uqlMaker = UQLMAKER(command=CommandList.alterGraph, commonParams=requestConfig)
		uqlMaker.setCommandParams(oldGraphName)
		data = {"name": newGraphName}
		if newDescription is not None:
			data.update({'description': newDescription})
		uqlMaker.addParam("set", data)
		res = self.uqlSingle(uqlMaker)
		return res
