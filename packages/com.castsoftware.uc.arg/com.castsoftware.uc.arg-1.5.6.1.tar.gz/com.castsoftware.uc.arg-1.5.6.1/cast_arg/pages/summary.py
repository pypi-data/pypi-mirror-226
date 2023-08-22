
from cast_common.highlight import Highlight
from cast_common.logger import Logger, INFO,DEBUG
from cast_common.powerpoint import PowerPoint

from pandas import json_normalize

class HighlightSummary(Highlight):

    def report(self,app_name:str,app_no:int,prs:PowerPoint,output:str) -> bool:
        df = json_normalize(self._get_metrics(app_name))

        app_tag = f'app{app_no}'

        for item in ['softwareResiliency','softwareAgility','softwareElegance','cloudReady','openSourceSafety']:
            data = float(round(df[item].iloc[0] * 100,1))
            self.replace_text(prs,app_tag,item,data)

        for item in ['totalFiles']:
            data = round(df[item].iloc[0],0)
            self.replace_text(prs,app_tag,item,data)

        tech = json_normalize(df['technologies'])
        self.replace_text(prs,'tech_count',item,len(tech.columns))

        for item in ['totalFiles','totalLinesOfCode','backFiredFP']:
            data = int(df[item].iloc[0])
            self.replace_text(prs,app_tag,item,data)

        prs.replace_text(f'{{{app_tag}_components}}',len(json_normalize(df['components'][0])))


        print (df.columns)


        pass

    def replace_text(self,prs, prefix, item, data):
        tag = f'{{{prefix}_{item}}}'
        self.log.debug(f'{tag}: {data}')
        prs.replace_text(tag,data)

# from os.path import abspath
# from cast_common.util import format_table
# from pandas import ExcelWriter

# ppt = PowerPoint(r'E:\work\Decks\highlight-test.pptx',r'E:\work\Decks\test\highlight.pptx')

# app = 'CollabServer'
                            
# hl = HighlightSummary('n.kaplan+insightsoftwareMinerva@castsoftware.com','vadKpBFAZ8KIKb2f2y',hl_instance=383,hl_base_url='https://app.casthighlight.com',log_level=DEBUG)
# hl.report(app,1,ppt,r'E:\work\Decks\test')
# ppt.save()

