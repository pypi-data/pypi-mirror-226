import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import MultiComparison
import numpy as np
import json

class Stat_Manager:
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe
        self.menu = {
        'kstest' : {
            'name' : 'Kolmogorov-Smirnov Test',
            'type' : '정규성',
            'group' : 1,
            'testfunc' : stats.kstest,
            'division' : None,
        },
        
        'shapiro' : {
            'name' : 'Shapiro-Wilks Test',
            'type' : '정규성',
            'group' : 1,
            'testfunc' : stats.shapiro,
            'division' : None,
        },
        
        'levene' : {
            'name' : 'Levene Test',
            'type' : '등분산성',
            'group' : 2,
            'testfunc' : stats.levene,
            'division' : None,
        },
        
        'ttest_ind' : {
            'name' : 'Indenpendent Samples T-test',
            'type' : '차이비교_집단간',
            'group' : 2,
            'testfunc' : stats.ttest_ind,
            'division' : '모수'
        },
        
        'ttest_rel' : {
            'name' : 'Dependent Samples T-test',
            'type' : '차이비교_집단내',
            'group' : 1,
            'testfunc' : stats.ttest_rel,
            'division' : '모수'
        },
        
        'mannwhitneyu' : {
            'name' : 'Mann-Whitney U Test',
            'type' : '차이비교_집단간',
            'group' : 2,
            'testfunc' : stats.mannwhitneyu,
            'division' : '비모수'
        },
        
        'wilcoxon' : {
            'name' : 'Wilcoxon-Signed Ranksum Test',
            'type' : '차이비교_집단내',
            'group' : 1,
            'testfunc' : stats.wilcoxon,
            'division' : '비모수'        
        },
        
        
        'f_oneway' : {
            'name' : 'One-way ANOVA',
            'type' : '차이비교_집단간',
            'group' : 3,
            'testfunc' : stats.f_oneway,
            'division' : '모수'
            
        },
        
        'kruskal' : {
            'name' : 'Kruskal-Wallis Test',
            'type' : '차이비교_집단간',
            'group' : 3,
            'testfunc' : stats.kruskal,
            'division' : '비모수'
            
        },
        
        'chi2_contingency' : {
            'name' : 'Chi-Square Test',
            'type' : '빈도분석',
            'group': 1,
            'testfunc' : stats.chi2_contingency,
            'division' : None
            },
        
        'z_normal' : {
            'name' : 'z-skeweness & z-kurtosis test',
            'type' : '정규성_예외',
            'group' : 1,
            'testfunc' : self.zscore_normality,
            'division' : None
            },
        
        'fmax' : {
            'name' : 'F-max Test',
            'type' : '등분산성_예외',
            'group' : 2,
            'testfunc' : self.fmax_test,
            'division' : None,
            },
        
        'pearsonr' : {
            'name' : '상관분석: Pearson r',
            'type' : '상관분석',
            'group' : 1,
            'testfunc' : self.r_forargs,
            'division' : None,
        },
        
        'spearmanr' : {
            'name' : '상관분석: Spearman r',
            'type' : '상관분석',
            'group' : 1,
            'testfunc' : self.r_forargs,
            'division' : None,
        }
    }
        
    def progress(self, method: str, vars: list, group_vars: str = None, group_names: list = None, posthoc: None = False):
        df = self.df.dropna(axis=0, how = 'any', subset = vars)
        testfunc = self.menu[method]['testfunc']
        group_fill = self.menu[method]['group']
        testtype = self.menu[method]['type']
        testname = self.menu[method]['name']
        testdivision = self.menu[method]['division']
        
        n = len(df)
        
        if testtype == '빈도분석':
            ser = pd.crosstab(df[vars[0]], df[vars[1]])
            re = testfunc(ser)
            s = re[0]
            p = re[1]
            s = round(s, 3)
            p = round(p, 3)

            print(f"\n{testname}")
            print(f"변수 : {vars[0]}, {vars[1]}")
            print(f"검정통계치 = {s}, p = {p}\n")
            
            return ser
        
        if testtype == '정규성':
            ser = df[vars[0]]
            print(f"\n{testname}")
            if method == 'kstest':
                s, p = testfunc(ser, 'norm')
                
                if n < 30:
                    print("표본 수가 30보다 적습니다. 다른 분석을 고려하십시오. ")
                
            else:
                s, p = testfunc(ser)
                
                if n >= 30:
                    print("표본 수가 30보다 많습니다. 다른 분석을 고려하십시오.")
            
            
            s = round(s, 3)
            p = round(p, 3)
            
            print(f"변수 : {vars[0]}")
            print(f"n = {n}")
            print(f"검정통계치 = {s}, p = {p}")
            
            if p <= .05 : 
                print("정규성 가정 미충족")
                
            else:
                print('정규성 가정 충족')
        
        if testtype == '등분산성':
            series = []
            for n in range(len(group_names)):
                ser = df.loc[df[group_vars] == group_names[n], vars[0]]
                series.append(ser)
            
            s, p = testfunc(*series)
            s = round(s, 3)
            p = round(p, 3)
            
            print(f"\n{testname}")
            print(f"집단변수 : {group_vars}")
            print(f"비교집단 : {group_names}")
            print(f"검정통계치 = {s}, p = {p}")
            
            
            if p <= .05 :
                print('등분산성 가정 미충족')
            else:
                print('등분산성 가정 충족')
                
        if testtype == '차이비교_집단내':
            ser1 = df[vars[0]]
            ser2 = df[vars[1]]
            
            ser1_m = ser1.mean().round(2)
            ser1_sd = ser1.std().round(2)
            ser1_med = ser1.median().round(2)
            
            ser2_m = ser2.mean().round(2)
            ser2_sd = ser2.std().round(2)
            ser2_med = ser2.median().round(2)
            
            s, p = testfunc(ser1, ser2)
            s = round(s, 3)
            p = round(p, 3)
            
            print(f"\n{testname}")
            print(f"변수 : {vars[0]}, {vars[1]}")
            print(f"n = {n}")
            print(f"{vars[0]}: mean = {ser1_m}, median = {ser1_med}, sd = {ser1_sd}")
            print(f"{vars[1]}: mean = {ser2_m}, median = {ser2_med}, sd = {ser2_sd}")
            print(f"검정통계치 = {s}, p = {p}")
            
        if testtype == '차이비교_집단간':
        
            if group_fill == 2:
                ser1 = df.loc[df[group_vars] == group_names[0], vars[0]]
                ser2 = df.loc[df[group_vars] == group_names[1], vars[0]]
                
                ser1_m = ser1.mean().round(2)
                ser1_sd = ser1.std().round(2)
                ser1_med = ser1.median().round(2)
                
                ser2_m = ser2.mean().round(2)
                ser2_sd = ser2.std().round(2)
                ser2_med = ser2.median().round(2)
                
                s, p = testfunc(ser1, ser2)
                s = round(s, 3)
                p = round(p, 3)
            
                print(f"\n{testname}")
                print(f"변수 : {vars[0]}")
                print(f"집단변수 : {group_vars}")
                print(f"비교집단 : {group_names[0]}, {group_names[1]}")
                print(f"{group_names[0]} n = {len(ser1)}: {vars[0]}: mean = {ser1_m}, median = {ser1_med}, sd = {ser1_sd}")
                print(f"{group_names[1]} n = {len(ser2)}: {vars[0]}: mean = {ser2_m}, median = {ser2_med}, sd = {ser2_sd}")
                print(f"검정통계치 = {s}, p = {p}")
                
            else:
                series = []
                for n in range(len(group_names)):
                    ser = df.loc[df[group_vars] == group_names[n], vars[0]]
                    series.append(ser)
                
                dict = {}
                for n in range(len(group_names)):
                    dict[group_names[n]] = {
                        'n' : len(series[n]),
                        'mean' : series[n].mean().round(2),
                        'median' : series[n].median().round(2),
                        'sd' : series[n].std().round(2),
                        }
                
                dict = json.dumps(dict, indent=4, ensure_ascii=False)
                
                s, p = testfunc(*series)
                s = round(s, 3)
                p = round(p, 3)
            
                print(f"\n{testname}")
                print(f"변수 : {vars[0]}")
                print(f"집단변수 : {group_vars}")
                print(f"비교집단 : {group_names}")
                print(f"집단별 기술통계치: \n{dict}")
                print(f"검정통계치 = {s}, p = {p}")
                
                
                if posthoc == True:
                    
                    cond_list = []
                    for n in range(len(group_names)):
                        cond = df[group_vars] == group_names[n]
                        cond_list.append(cond)
                    
                    
                    selected_rows = pd.concat(cond_list, axis=1).any(axis=1)
                    selected_df = df[selected_rows]
                    
                    mc = MultiComparison(selected_df[vars[0]], selected_df[group_vars])
                    
                    
                    if testdivision == '모수':
                        result = mc.allpairtest(stats.ttest_ind, method = 'bonf')
                    else: 
                        result = mc.allpairtest(stats.mannwhitneyu, method = 'bonf')
                    
                    print('\nPost-hoc 실시')
                    return result[0]
                
        if testtype == '정규성_예외':
            print(f"{testname}")
            print(f"변수: {vars[0]}")
            testfunc(self.df[vars[0]])
            
        if testtype == '등분산성_예외':
            print(f"{testname}")
            print(f"변수: {vars[0]}")
            testfunc(vars = vars, group_vars = group_vars, group_names = group_names)
            
        if testtype == '상관분석':
            print(testname)
            print(f"변수 : {vars}\n")
            testfunc(method = method, vars = vars)
            
            if method == 'pearsonr':
                return df[vars].corr().round(3)
    
    def zscore_normality(self, series):
        n = series.count()
        
        skewness = series.skew().round(3)
        skewness_se = np.sqrt(6 * n * (n - 1) / ((n - 2) * (n + 1) * (n + 3))).round(3)
        
        kurtosis = series.kurtosis().round(3)
        kurtosis_se = (np.sqrt((n**2 - 1) / ((n-3)*(n+5))) * skewness_se * 2).round(3)
        
        z_skewness = (skewness/skewness_se).round(3)
        z_kurtosis = (kurtosis/kurtosis_se).round(3)
        
        if n < 50:
            cutoff = 1.96
        elif n < 200:
            cutoff = 2.59
        elif n > 200:
            cutoff = 3.13
        
        print(f"skewness = {skewness}\nstandard error of skewness = {skewness_se}\nz-skewness = {z_skewness}\n\nkurtosis = {kurtosis}\nstandard error of kurtosis = {kurtosis_se}\nz-kurtosis = {z_kurtosis}\n\nsample n = {n}, corresponding absolute cutoff score of z-skewenss and z-kurtosis = {cutoff}")
        
        z_skewness = abs(z_skewness)
        z_kurtosis = abs(z_kurtosis)
        
        print("\n결과: ")
        if z_skewness < cutoff and z_kurtosis < cutoff:
            print("\n정규성 가정 충족")
        else:
            print("\n정규성 가정 미충족")
            
            
        print("\nReferences:\n[1] Ghasemi, A., & Zahediasl, S. (2012). Normality tests for statistical analysis: a guide for non-statisticians. International journal of endocrinology and metabolism, 10(2), 486. \n[2] Moon, S. (2019). Statistics for the Social Sciences: Moving Toward an Integrated Approach. Cognella Academic Publishing.")
        
    def fmax_test(self, vars, group_vars, group_names):
        df = self.df.loc[self.df[group_vars].isin(group_names)]
        group_n = len(group_names)
        
        max_variance = df.groupby(group_vars)[vars[0]].var().max().round(3)
        min_variance = df.groupby(group_vars)[vars[0]].var().min().round(3)
        
        f_max = max_variance / min_variance
        f_max = round(f_max, 3)
        
        
        print(f"\n집단 수 = {group_n}")
        print(f"Max variance among group = {max_variance}")
        print(f"Min variance among group = {min_variance}")
        print(f"F-max statistics = {f_max}\n")
        print("\n결론:")
        
        if f_max < 10:
            print("등분산성 가정 충족")
        else:
            print("등분산성 가정 미충족")
            
        print("\nReference:\n[1] Fidell, L. S., & Tabachnick, B. G. (2003). Preparatory data analysis. Handbook of psychology: Research methods in psychology, 2, 115-141.\n")
    
    def r_forargs(self, method, vars):
        df = self.df.dropna(axis=0, how = 'any', subset = vars)
        
        if method == 'pearsonr':
            tf = stats.pearsonr
        
        elif method == 'spearmanr':
            tf = stats.spearmanr
        
        num = len(vars)
        sets = []
        
        for i in range(num -1):
            for j in range(i +1, num):
                sets.append((df[vars[i]], df[vars[j]]))
            
        for n in sets:
            s, p = tf(n[0], n[1])
            s = round(s, 3)
            p = round(p, 3)
            var1 = n[0].name
            var2 = n[1].name
            
            print(f"{var1} & {var2} r = {s}, p = {p}")
