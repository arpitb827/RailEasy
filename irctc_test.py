from irctc import RAIL_API
# import pandas as np
# import matplotlib.pyplot as plt

result = RAIL_API("http://api.railwayapi.com/",'mia22f6h')

response = result.get_train_live_status(12953,20170614)

print "response=============",response,type(response)
print "keys======",response.keys()

#starting pandas for analytics
# p_data = np.DataFrame(response['current_station'])

# p_data = np.DataFrame.from_dict(response['route'], orient='index')
# print "p_data===============\n",p_data

# ax = df[['V1','V2']].plot(kind='bar', title ="V comp", figsize=(15, 10), legend=True, fontsize=12)