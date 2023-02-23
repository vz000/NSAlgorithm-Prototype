import pandas as pd
from matplotlib import pyplot as plt

data_file = 'permissions-gw.csv' # csv file with permissions
pd.set_option('display.float_format','{:.0f}'.format)
anomallies = pd.DataFrame({'Cause':[],
                         'Incidence':[]})
permissions_quantity = pd.DataFrame({'Quantity':[]})
permissions_limit = 50
df_permissions = pd.DataFrame({'Permission':[],
                                'Times':[]})

def plot_density(permissions):
    fig = plt.figure()
    permissions['Quantity'].plot(kind='density')
    plt.show()

print(df_permissions.head(10))
def data_stat_values(permissions_numbers):
    permissions_numbers = permissions_numbers['Quantity']
    permissions_mode = permissions_numbers.mode()
    permissions_min = permissions_numbers.min()
    permissions_max = permissions_numbers.max()
    print("Mode: {:.0f}\nMin: {:.0f}\nMax: {:.0f}".format(permissions_mode[0],permissions_min,permissions_max))
    std = permissions_numbers.std()
    print("Standard deviation: ", std) # too high when there is no limiti in permission quantity

def get_permission_count(permissions, df_permissions):
    local_df = df_permissions
    for permission in permissions:
        permission = permission.rstrip()
        permission_empty = local_df[local_df['Permission']==permission]
        if permission_empty.empty:
            local_df = pd.concat([local_df,pd.DataFrame({'Permission':[permission],
                                                                    'Times':1})], ignore_index=True)
        else:
            index = local_df.index[local_df['Permission'] == permission][0]
            local_df.at[index,'Times'] = local_df.at[index,'Times'] + 1
    return local_df

with open(data_file,'r') as permissions:
    for row in permissions:
        permissions = row.split(",")
        permissions_len = len(permissions)
        # with a limit of permissions_limit = 50, only 12 samples (8 ransomware, 4 goodware) 
        # would be inmediately classified as ransomware.
        if(permissions_len > permissions_limit):
            anomallies = pd.concat([anomallies,pd.DataFrame({'Cause':['Total permissions: '+ str(permissions_len)],
                                     'Incidence':['Too many permissions']})], ignore_index=True)
        if(permissions_len >= 1 and permissions_len < permissions_limit):
            permissions_quantity = pd.concat([permissions_quantity,pd.DataFrame({'Quantity':[permissions_len]})], 
                                      ignore_index=True)
            df_permissions = get_permission_count(permissions, df_permissions)

data_stat_values(permissions_quantity)
# plot_density(permissions_quantity)
print(permissions_quantity.shape)
df_permissions = df_permissions.sort_values(by=['Times'],ascending=False)
print(df_permissions['Permission'].head(15))
print(anomallies)
