import requests
URL = 'http://0.0.0.0:8080/'

response = requests.get(f'{URL}health')
print(response)

# create new user
# if response.status_code == 200:
#     for user_num in range(1, 4):
#         response = requests.post(f'{URL}new_user',
#                                  json={
#                                      'user_name': f'user_{user_num}',
#                                      'password': '12333Sdf545sdf'
#                                  })
#         print(f'create:\n {response.json()}')


# get user fo id
# get_user = requests.get(f'{URL}get_user/1')
# print(get_user)
# print(f'get_user: {get_user.json()}')

# create advertisement
create_advertisement = requests.post(f'{URL}adv_new',
                                     json={
                                         'title': 'thing_6',
                                         'description': 'ttu',
                                         'user_name': 'user_2',
                                         'password': '12333Sdf545sdf',
                                     })
print('____create_advertisement____')
print(create_advertisement)
print(create_advertisement.json())

get_advertisement_all = requests.get(f'{URL}adv')
print('\n____get_advertisement_all____')
print(get_advertisement_all)
print(get_advertisement_all.json())

#
# get_advertisement_1 = requests.get(f'{URL}adv/1')
# print('\n____get_advertisement_1____')
# print(get_advertisement_1)
# print(get_advertisement_1.json())

#
# del_advertisement_1 = requests.delete(f'{URL}adv_del/1', json={
#                                          'user_name': f'user_1',
#                                          'password': '12333Sdf545sdf'
#                                      })
# print('____del_advertisement_1___')
# print(del_advertisement_1)
# print(del_advertisement_1.json())

# patch_advertisement_2 = requests.patch(f'{URL}adv_patch/2',
#                                        json={
#                                            'user_name': f'user_1',
#                                            'password': '12333Sdf545sdf',
#                                            'title': '4rfff'
#                                        })
# print('\n____patch_advertisement_1____')
# print(patch_advertisement_2)
# print(patch_advertisement_2.json())