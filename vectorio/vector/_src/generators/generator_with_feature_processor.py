#!-*-coding:utf-8-*-


class GeneratorWithFeatureProcessor:

    def __new__(self, *args, **kwargs):
        datasource = args[0]
        features_qtd_by_lyr = 0
        feature_to_specific_geo_data = yield  # getting data from 'send'
        yield  # stoping next iteration

        for idx_lyr in range(datasource.GetLayerCount()):
            features_qtd_by_lyr = datasource.GetLayer(
                idx_lyr
            ).GetFeatureCount()
            for idx_feat in range(features_qtd_by_lyr):
                feat = datasource.GetLayer(idx_lyr).GetFeature(idx_feat)
                yield feature_to_specific_geo_data(feat)
