import pdfplumber
import pandas as pd

def parse_results():
    pdf = pdfplumber.open('ResultListsOverallResults.pdf')

    results = []

    ts = {'vertical_strategy': 'text', 'horizontal_strategy': 'text', 'text_x_tolerance': 3, 'text_y_tolerance': 1}
    left_end = 73
    right_end = 140
    p1_top = 130
    pother_top = 110
    for page_num, page in enumerate(pdf.pages):
        if page_num == 0:
            pcl = page.crop((0,p1_top,left_end,page.height))
            pcr = page.crop((right_end,130,page.width,page.height))
        else:
            pcl = page.crop((0,pother_top,left_end,page.height))
            pcr = page.crop((right_end,110,page.width,page.height))
        tl = pcl.extract_table(ts)
        tr = pcr.extract_table(ts)
        for r in zip(tl,tr):
            if r[0][0].isnumeric():
                results.append(r[0]+r[1][0:2]+r[1][-4:])

    return results

def main():
    results = parse_results()
    df = pd.DataFrame(results, columns=['Overall','Gender_Place','Bib','Name','Age','Gender','Time','Pace'])
    df.to_csv('Skate2023.csv')
    
    
    #df = pd.read_csv('Skate2023.csv')
    #print(df.head())

if __name__ == "__main__":
    main()
