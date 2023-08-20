from macrocorr.utils import *
from collections import defaultdict

class macroIndicator:

    """
    #0: API name
    #1: 0= yahooFinance; 1= World Bank
    #2: 0= no_input; 1= country
    #3: population, development, economy, finance, internaitonal, commodity, 
    """

    mi_dict_temp = {
        "Agricultural raw materials imports": ["TM.VAL.AGRI.ZS.UN", 1, 1, 'internaitonal'],
        "Basic drinking water services": ["SH.H2O.BASW.ZS", 1, 1, 'development'],
        "Battle-related deaths": ["VC.BTL.DETH", 1, 1, 'development'],
        "Birth rate, crude": ["SP.DYN.CBRT.IN", 1, 1, 'population'],
        "Bonds": ["DT.NFL.PBND.CD", 1, 1, 'finance'],
        "Central Government Debt": ["GC.DOD.TOTL.GD.ZS", 1, 1, 'economy'],
        "CPI Price": ["PA.NUS.PPPC.RF", 1, 1, 'finance'],
        "Current account balance": ["BN.CAB.XOKA.CD", 1, 1, 'internaitonal'],
        "Current education expenditure": ["SE.XPD.CTOT.ZS", 1, 1, 'development'],
        "Current health expenditure per capita": ["SH.XPD.CHEX.GD.ZS", 1, 1, 'development'],
        "Days to obtain an operating license": ["IC.FRM.DURS", 1, 1, 'economy'],
        "Death rate, crude": ["SP.DYN.CDRT.IN", 1, 1, 'population'],
        "Electric power consumption": ["EG.ELC.ACCS.ZS", 1, 1, 'development'],
        "Employment in agriculture": ["SL.AGR.EMPL.ZS", 1, 1, 'economy'],
        "Employment to population ratio": ["SL.EMP.TOTL.SP.NE.ZS", 1, 1, 'economy'],
        "Export volume index": ["TX.QTY.MRCH.XD.WD", 1, 1, 'internaitonal'],
        "Food imports": ["TM.VAL.FOOD.ZS.UN", 1, 1, 'internaitonal'],
        "Foreign direct investment": ["BN.KLT.DINV.CD", 1, 1, 'internaitonal'],
        "Fuel exports": ["TX.VAL.FUEL.ZS.UN", 1, 1, 'internaitonal'],
        "GDP": ["NY.GDP.MKTP.CD", 1, 1, 'economy'],
        "GDP per capita": ["NY.GDP.PCAP.KN", 1, 1, 'economy'],
        "GNI": ["NY.GNP.MKTP.CD", 1, 1, 'economy'],
        "GNI per capita": ["NY.GNP.PCAP.CD", 1, 1, 'economy'],
        "Government expenditure on education": ["SE.XPD.TOTL.GB.ZS", 1, 1, 'development'],
        "Gross savings": ["NY.GNS.ICTR.CD", 1, 1, 'finance'],
        "High Technology Export": ["TX.VAL.TECH.CD", 1, 1, 'internaitonal'],
        "Import volume index": ["TM.QTY.MRCH.XD.WD", 1, 1, 'internaitonal'],
        "Industry, Value Added": ["NV.IND.TOTL.ZS", 1, 1, 'economy'],
        "International migrant stock": ["SM.POP.TOTL", 1, 1, 'internaitonal'],
        "International tourism": ["ST.INT.ARVL", 1, 1, 'internaitonal'],
        "Labor force participation rate": ["SL.TLF.ACTI.ZS", 1, 1, 'economy'],
        "Life expectancy": ["SP.DYN.LE00.IN", 1, 1, 'population'],
        "Literacy rate": ["SE.ADT.LITR.ZS", 1, 1, 'development'],
        "Net Financial Account": ["BN.FIN.TOTL.CD", 1, 1, 'finance'],
        "Net primary income": ["NY.GSR.NFCY.CD", 1, 1, 'economy'],
        "Number of infant deaths": ["SH.DTH.IMRT", 1, 1, 'population'],
        "Number of Physicians": ["SH.MED.PHYS.ZS", 1, 1, 'development'],
        "Official exchange rate": ["PA.NUS.FCRF", 1, 1, 'internaitonal'],
        "Population, total": ["SP.POP.TOTL", 1, 1, 'population'],
        "Population ages 15-64": ["SP.POP.1564.TO", 1, 1, 'population'],
        "Population density": ["EN.POP.DNST", 1, 1, 'population'],
        "Population, female": ["SP.POP.TOTL.FE.IN", 1, 1, 'population'],
        "Population, male": ["SP.POP.TOTL.MA.IN", 1, 1, 'population'],
        "Poverty headcount ratio at national poverty line": ["SI.POV.NAHC", 1, 1, 'economy'],
        "Profit tax": ["IC.TAX.PRFT.CP.ZS", 1, 1, 'finance'],
        "Rural population": ["SP.RUR.TOTL", 1, 1, 'population'],
        "School enrollment": ["SE.TER.ENRR", 1, 1, 'development'],
        "Stock Traded": ["CM.MKT.TRAD.CD", 1, 1, 'finance'],
        "Suicide mortality rate": ["SH.STA.SUIC.P5", 1, 1, 'population'],
        "Tariff rate": ["TM.TAX.MANF.SM.AR.ZS", 1, 1, 'internaitonal'],
        "Tax revenue": ["GC.TAX.TOTL.GD.ZS", 1, 1, 'economy'],
        "Total alcohol consumption per capita": ["SH.ALC.PCAP.LI", 1, 1, 'economy'],
        "Unemployment": ["SL.UEM.TOTL.NE.ZS", 1, 1, 'economy'],
        "Urban population": ["SP.URB.TOTL", 1, 1, 'population'],
        "Women Business and the Law Index Score": ["SG.LAW.INDX", 1, 1, 'development'],
        "Gold": ["GC=F", 0, 0, 'commodity'],
        "Silver": ["SI=F", 0, 0, 'commodity'],
        "Platinum": ["PL=F", 0, 0, 'commodity'],
        "Copper": ["HG=F", 0, 0, 'commodity'],
        "Palladium": ["PA=F", 0, 0, 'commodity'],
        "Crude Oil": ["CL=F", 0, 0, 'commodity'],
        "Heating Oil": ["HO=F", 0, 0, 'commodity'],
        "Natural Gas ": ["NG=F", 0, 0, 'commodity'],
        "RBOB Gasoline ": ["RB=F", 0, 0, 'commodity'],
        "Corn": ["ZC=F", 0, 0, 'commodity'],
        "Oat": ["ZO=F", 0, 0, 'commodity'],
        "Wheat": ["KE=F", 0, 0, 'commodity'],
        "Rice": ["ZR=F", 0, 0, 'commodity'],
        "Soybean": ["ZS=F", 0, 0, 'commodity'],
        "Live Cattle": ["LE=F", 0, 0, 'commodity'],
        "Cocoa": ["CC=F", 0, 0, 'commodity'],
        "Coffee ": ["KC=F", 0, 0, 'commodity'],
        "Cotton": ["CT=F", 0, 0, 'commodity'],
        "Sugar": ["SB=F", 0, 0, 'commodity'],
        "Luxury Goods": ["^LUXURY.REGA", 0, 0, 'commodity'],
        "NASDAQ Composite": ["^IXIC", 0, 0, 'finance'],
        "S&P 500": ["^GSPC", 0, 0, 'finance'],
        "Dow Jones Industrial Average": ["^DJI", 0, 0, 'finance'],
        "NYSE Composite": ["^NYA", 0, 0, 'finance'],
        "Cboe UK 100": ["^BUK100P", 0, 0, 'finance'],
        "Russell 2000": ["^RUT", 0, 0, 'finance'],
        "CBOE Volatility Index": ["^VIX", 0, 0, 'finance'],
        "STI Index": ["^STI", 0, 0, 'finance'],
        "Treasury Yield 10 Years": ["^TNX", 0, 0, 'finance'],
        "NASDAQ 100 Technology Sector": ["^NDXT", 0, 0, 'finance'],
        "NASDAQ Insurance": ["^INSR", 0, 0, 'finance'],
        "Bitcoin": ["BTC-USD", 0, 0, 'finance'],
    }

    num_of_categories = 7
    categories = defaultdict(list)

    mi_dict={}
    for key, value in mi_dict_temp.items():
        uniform_key=utils.filter_string(key)
        mi_dict[uniform_key]=value
        categories[value[-1]].append(uniform_key)
        mi_dict[uniform_key].append(key)
    
    del mi_dict_temp

