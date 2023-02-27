import pandas as pd

class Permission_Stats():
    def __init__(self, file_name):
        self.data_file = file_name # csv file with permissions
        pd.set_option('display.float_format','{:.0f}'.format)
        self.anomallies = pd.DataFrame({'Cause':[],
                                'Incidence':[]})
        self.permissions_quantity = pd.DataFrame({'Quantity':[]})
        self.permissions_limit = 50
        self.df_permissions = pd.DataFrame({'Permission':[],
                                        'Times':[]})
        self.read_permission_list()

    def get_permission_count(self,permissions):
        for permission in permissions:
            permission = permission.rstrip()
            permission_empty = self.df_permissions[self.df_permissions['Permission']==permission]
            if permission_empty.empty:
                self.df_permissions = pd.concat([self.df_permissions,pd.DataFrame({'Permission':[permission],
                                                                        'Times':1})], ignore_index=True)
            else:
                index = self.df_permissions.index[self.df_permissions['Permission'] == permission][0]
                self.df_permissions.at[index,'Times'] = self.df_permissions.at[index,'Times'] + 1

    def read_permission_list(self):
        with open(self.data_file,'r') as permissions:
            for row in permissions:
                permissions = row.split(",")
                permissions_len = len(permissions)
                if(permissions_len > self.permissions_limit):
                    self.anomallies = pd.concat([self.anomallies,pd.DataFrame({'Result':['Total permissions: '+ str(permissions_len)],
                                            'Problem':['Too many permissions']})], ignore_index=True)
                if(permissions_len >= 1 and permissions_len < self.permissions_limit):
                    self.permissions_quantity = pd.concat([self.permissions_quantity,pd.DataFrame({'Quantity':[permissions_len]})], 
                                            ignore_index=True)
                    self.get_permission_count(permissions)
        self.df_permissions = self.df_permissions.sort_values(by=['Times'],ascending=False)
        self.df_permissions['Permission'].head(15).to_csv('common-permissions-rw.csv', index=False, header=False)
