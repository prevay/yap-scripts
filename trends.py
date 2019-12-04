import matplotlib.pyplot as plt
import pandas as pd
import os


def chart(varcodes, measure, labels=None, from_date=2014, to_date=2018, title=None):

    plt.rcParams['figure.figsize'] = [10, 5]

    foldernames = ['DS0001', 'DS0002', 'DS0003', 'DS0004',
                   'DS0005', 'DS0006', 'DS0007']


    varcodes = varcodes.split(',')
    labels = labels.split(',')
    trends_dict = {code: list() for code in varcodes}
    years = range(from_date, to_date + 1)

    for i in years:
        for code in varcodes:
            total_occurences = 0
            data_size = 0
            for foldername in foldernames:
                filename = next(file for file in os.listdir('Monitoring_the_Future/{0}/{1}/'.format(i, foldername))
                                if file.endswith('.tsv'))
                with open('Monitoring_the_Future/{0}/{1}/{2}'.format(i, foldername, filename)) as f:
                    volume_df = pd.read_csv(f, sep='\t')
                    if code in list(volume_df.columns):
                        valid_data = volume_df[code][volume_df[code] != -9]
                        if measure[0] == '=':
                            occurences = valid_data[valid_data == int(measure[1])].size
                        elif measure[0] == '>':
                            occurences = valid_data[valid_data > int(measure[1])].size
                        elif measure[0] == '<':
                            occurences = valid_data[valid_data > int(measure[1])].size
                        else:
                            print('Invalid comparison operator')
                        total_occurences += occurences
                        data_size += valid_data.size
            trends_dict[code].append(total_occurences/data_size)

    for code in varcodes:
        plt.plot(list(years), trends_dict[code])
    plt.xticks(years)
    plt.legend(labels)
    plt.title(title)
    plt.show()


if __name__ == "__main__":

    chart('V2101,V2104,V2115',labels='Cigarettes,Alcohol,Marijuana', measure='>1',
          title="% of teens that have ever used the following substances")
