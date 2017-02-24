#coding:utf-8

#(seconds 60**2 == 1 hour)
"""
######### manage_some config ############################################
spider every one's config
"""
########live_dynamic config
DYNAMIC_TIME = 60*10

########goods_info config
GOODS_INFO_TIME = 60**2

########update_goods_id config 
UPDATE_GOODS_ID_TIME = 60**2*0.5

#######sleep and detect config
SLEEP_DETECT_TIME = 60*10

"""
############## manage_all config ########################################
update zhubo and goods's config
"""

########update_zhubo_info config
UPDATE_ZHUBO_INFO_TIME = 60**2*24*30

########update_goods_info config
UPDATE_GOODS_INFO_TIME = 60**2*4


"""
############## manage_list config ########################################
update zhubo config
"""


#########update_zhubo_from_db config
UPDATE_ZHUBO_LIVE_TIME = 60**2

"""
#########process num ##########################
"""
PROCESS_NUM = 8