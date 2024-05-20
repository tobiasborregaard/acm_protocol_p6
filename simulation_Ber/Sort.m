data = readtable("thrAPRROXTABLE2024_04_24-10_36.csv", 'HeaderLines', 1);
data.Properties.VariableNames = {'MODCOD','GP','THR'};


Tsort = sortrows(data,'THR');

writetable(Tsort,'thrAPRROXTABLE2024_04_24-10_36.csv')



