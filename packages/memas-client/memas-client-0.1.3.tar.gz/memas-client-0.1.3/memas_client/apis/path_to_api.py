import typing_extensions

from memas_client.paths import PathValues
from memas_client.apis.paths.dp_memorize import DpMemorize
from memas_client.apis.paths.dp_recall import DpRecall

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.DP_MEMORIZE: DpMemorize,
        PathValues.DP_RECALL: DpRecall,
    }
)

path_to_api = PathToApi(
    {
        PathValues.DP_MEMORIZE: DpMemorize,
        PathValues.DP_RECALL: DpRecall,
    }
)
