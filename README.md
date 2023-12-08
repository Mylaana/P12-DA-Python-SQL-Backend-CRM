# P12-DA-Python-SQL-Backend-CRM

todo :
update docstrings
add sentry
write readme


---------- coverage: platform win32, python 3.11.7-final-0 -----------    
Name                                                                    Stmts   Miss  Cover
-------------------------------------------------------------------------------------------
Client\__init__.py                                                        
  0      0   100%
Client\admin.py                                                           
  5      0   100%
Client\apps.py                                                            
  4      0   100%
Client\management\__init__.py                                             
  0      0   100%
Client\management\commands\__init__.py                                    
  0      0   100%
Client\management\commands\client.py                                      
121     28    77%
Client\migrations\0001_initial.py                                         
  7      0   100%
Client\migrations\0002_client_date_update_client_information.py           
  4      0   100%
Client\migrations\__init__.py                                             
  0      0   100%
Client\models.py                                                          
 14      1    93%
Contract\__init__.py                                                      
  0      0   100%
Contract\admin.py                                                         
  5      0   100%
Contract\apps.py                                                          
  4      0   100%
Contract\management\__init__.py                                           
  0      0   100%
Contract\management\commands\__init__.py                                  
  0      0   100%
Contract\management\commands\contract.py                                  
132     28    79%
Contract\migrations\0001_initial.py                                       
  7      0   100%
Contract\migrations\0002_alter_contract_value_rest_to_pay_and_more.py       4      0   100%
Contract\migrations\__init__.py                                           
  0      0   100%
Contract\models.py                                                        
 13      1    92%
EpicEvents\__init__.py                                                    
  2      0   100%
EpicEvents\authentication.py                                              
 56     17    70%
EpicEvents\settings.py                                                    
 26      0   100%
EpicEvents\utils.py                                                       
117     11    91%
Event\__init__.py                                                         
  0      0   100%
Event\admin.py                                                            
  5      0   100%
Event\apps.py                                                             
  4      0   100%
Event\management\__init__.py                                              
  0      0   100%
Event\management\commands\__init__.py                                     
  0      0   100%
Event\management\commands\event.py                                        
142     31    78%
Event\migrations\0001_initial.py                                          
  7      0   100%
Event\migrations\0002_alter_event_attendees.py                            
  4      0   100%
Event\migrations\0003_alter_event_contract.py                             
  5      0   100%
Event\migrations\__init__.py                                              
  0      0   100%
Event\models.py                                                           
 14      1    93%
UserProfile\admin.py                                                      
  9      0   100%
UserProfile\apps.py                                                       
  4      0   100%
UserProfile\management\__init__.py                                        
  0      0   100%
UserProfile\management\commands\__init__.py                               
  0      0   100%
UserProfile\management\commands\team.py                                   
 90     14    84%
UserProfile\management\commands\user.py                                   
112     16    86%
UserProfile\migrations\0001_initial.py                                    
  5      0   100%
UserProfile\migrations\0002_team_userprofile_team.py                      
  5      0   100%
UserProfile\migrations\__init__.py                                        
  0      0   100%
UserProfile\models.py                                                     
 43     21    51%
tests\__init__.py                                                         
  0      0   100%
tests\client\__init__.py                                                  
  0      0   100%
tests\client\commands\__init__.py                                         
  0      0   100%
tests\client\commands\test_integration_client.py                          
 41      0   100%
tests\client\commands\test_integration_client_handle.py                   
 44      0   100%
tests\conftest.py                                                         
 35      0   100%
tests\contract\__init__.py                                                
  0      0   100%
tests\contract\commands\__init__.py                                       
  0      0   100%
tests\contract\commands\test_integration_contract.py                      
 50      0   100%
tests\epicevents\__init__.py                                                0      0   100%
tests\epicevents\test_unit_authentication.py                               20      0   100%
tests\epicevents\test_unit_utils.py                                         9      0   100%
tests\event\__init__.py                                                     0      0   100%
tests\event\commands\__init__.py                                            0      0   100%
tests\event\commands\test_integration_event.py                             42      0   100%
tests\event\commands\test_integration_event_handle.py                      41      0   100%
tests\fixtures.py                                                          12      1    92%
tests\userprofile\__init__.py                                               0      0   100%
tests\userprofile\commands\__init__.py                                      0      0   100%
tests\userprofile\commands\test_integration_team_handle.py                 39      0   100%
tests\userprofile\commands\test_integration_userprofile.py                 46      0   100%
tests\userprofile\commands\test_integration_userprofile_handle.py          43      0   100%
-------------------------------------------------------------------------------------------
TOTAL                                                                    1432    170    88%