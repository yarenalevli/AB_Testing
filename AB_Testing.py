
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import  shapiro, levene, ttest_ind

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

################################################
#Task 1: Define the hypothesis of the A/B test.
################################################
df_control = pd.read_excel("Datasets/ab_testing.xlsx", sheet_name="Control Group")
df_test = pd.read_excel("Datasets/ab_testing.xlsx", sheet_name="Test Group")

def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Describe #####################")
    print(dataframe.describe().T)

check_df(df_control)
check_df(df_test)

def plot(dataframe):
    sns.distplot(dataframe)
    plt.show()

plot(df_control.Purchase)
plot(df_test.Purchase)

# Assumption Control
# if p-value < 0.05, then H0 is REJECTED.
# if p-value > 0.05, H0 CANNOT BE REJECTED.
# H0: The normal distribution assumption is provided.
# H1:..it is not provided.

def shapirotest(dataframe):
    test_stat, pvalue = shapiro(dataframe)
    print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

shapirotest(df_control.Purchase) # p-value = 0.58, H0 can not be rejected.
shapirotest(df_test.Purchase) # p-value = 0.15, H0 can not be rejected.
# The normal distribution assumption is provided.

# The Assumption of Uniformity of Variance
test_stat, pvalue = levene(df_control["Purchase"].dropna(),
                           df_test["Purchase"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue)) # p-value = 0.1, H0 can not be rejected.

# Hypothesis Testing
# 1. If assumptions are provided, an independent two-sample t-test (parametric test)
# 2. Mannwhitneyu test (non-parametric test) if assumptions are not provided

# We will apply Parametric testing because Variance is provided in the applications we make.

test_stat, pvalue = ttest_ind(df_control['Purchase'],
                              df_test['Purchase'],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value = 0.34, H0 can not be rejected.

# Conversion Rate:
# Click/Impression

conversion_rate_control = ((df_control["Click"] / df_control["Impression"]) * 100).mean() # 5.36
conversion_rate_test =((df_test["Click"] / df_test["Impression"]) * 100).mean() # 3.41

################################################
#TASK 2: Comment on whether the test results obtained are statistically significant.
################################################
"""
According to the test results, our p-value is more than 0.05 from the significance level. Therefore, we cannot reject 
the hypothesis. This means that according to our A/B test, the average of the two groups does not statistically differ from each other, 
leaving no room for luck. So, is the same.
"""
################################################
#TASK 3: What tests did you use? Specify the reasons.
################################################
"""
1. The Shapiro Wilk test is used when performing the assumption control.
2. The Levene test is used to check the Uniformity of Variance, since the normality assumptions of the control result 
are provided.
3. Finally, Two Sample T Tests (Parametric Tests) are used, regardless of which assumptions are provided.
"""
################################################
#TASK 4: According to the answer you gave in Task 2, what is your advice to the client?
################################################
"""
According to our A/B test, the average of the two groups does not statistically differ from each other without leaving room for luck
we have reached the conclusion. Therefore, my suggestion is that averagebidding is less of a click-through rate than maximumbidding
I suggest that it is appropriate for them to stay in the maximumbidding system.
"""



