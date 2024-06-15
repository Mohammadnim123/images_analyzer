from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .services import SkinImagesAnalyzerService

class SkinImagesAnalyzerView(ViewSet):

    @action(['get'], detail=False)
    def test_view(self, request):
        res = SkinImagesAnalyzerService.test_view()
        return Response(res)