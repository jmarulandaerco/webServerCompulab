from django.contrib import admin
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView) 
from django.urls import path
from AppFrontend.Views.checkPassWordView import ChangePassword, CheckPassword
from AppFrontend.Views.contenView import ContentView, ContentViewMenuChecker, ContentViewMenuCompensationLimitation, ContentViewMenuDatabase, ContentViewMenuMain, ContentViewMenuModbus, ContentViewMenuSetting
from AppFrontend.Views.deleteView import DeleteCollectionView,DeleteLog
from AppFrontend.Views.homeView import HomeView
from AppFrontend.Views.settingSystemView import AddWifi, AntennaWifi, InterfaceConnection
from AppFrontend.Views.jsonView import ListColections
from AppFrontend.Views.logView import GetLogsView, LogTemplateView
from AppFrontend.Views.loginView import IndexView
from AppFrontend.Views.menuView import FormDataBasePropierties, FormDataCompensation, FormDataLimitation, FormDataModemChecker, FormDataModes, FormDataServer, FormDataServerChecker, FormDataSettingDataBase, FormDataSettingInterface, FormDataSettingLogs, FormDataSignalChecker, MeasureView
from AppFrontend.Views.modbusView import FormModbusAddDeviceRtu, FormModbusAddDeviceTcp, FormModbusDeviceRtuView, FormModbusDevicesView, FormModbusGetDevicesView, FormModbusView
from AppFrontend.Views.modemView import ModemView
from authApp.views.userDetailView import UserDetailView
from energyAPP.views.inverterDataView import InverterDataView
from energyAPP.views.serviceView import Reboot, StartView, StatusService, StopView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('home/content/<str:option>/', ContentView.as_view(), name='get_content'),
    path('home/content/form/<str:option>/', ContentViewMenuMain.as_view(), name='get_content_form_modbus_menu'),
    path('home/content/form/modbus/<str:option>/', ContentViewMenuModbus.as_view(), name='get_content_form_menu_modbus'),
    path('home/content/form/compensation-limitation/<str:option>/', ContentViewMenuCompensationLimitation.as_view(), name='get_content_form_compensation-limitation'),
    path('home/content/form/database/<str:option>/', ContentViewMenuDatabase.as_view(), name='get_content_form_database'),
    path('home/content/form/checker/<str:option>/', ContentViewMenuChecker.as_view(), name='get_content_form_checker'),
    path('home/content/form/setting/<str:option>/', ContentViewMenuSetting.as_view(), name='get_content_form_checker'),

    path('user/', UserDetailView.as_view(), name='user'),
    path('user/<str:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/inverter-data/', InverterDataView.as_view(), name='inverter-data'),
    path('home/start/', StartView.as_view(), name='start_service'),
    path('home/stop/', StopView.as_view(), name='stop_service'),
    path('home/reboot/', Reboot.as_view(), name='reboot_erco_pulse'),
    path('home/status/', StatusService.as_view(), name='status_service'),

    path("home/logs/", LogTemplateView.as_view(), name="log_view"),
    path("home/api/logs/", GetLogsView.as_view(), name="get_logs"),
    path('api/get-form-data/', MeasureView.as_view(), name='get_form_data'),
    path('api/get-form-data-server/', FormDataServer.as_view(), name='get_form_data_server'),
    path('api/get-form-data-modes/', FormDataModes.as_view(), name='get_form_data_modes'),
    path('api/get-form-data-setting-database/', FormDataSettingDataBase.as_view(), name='get_form_data_setting_database'),
    path('api/get-form-data-setting-interface/', FormDataSettingInterface.as_view(), name='get_form_data_setting_interface'),
    path('api/get-form-data-modem-checker/', FormDataModemChecker.as_view(), name='get_form_data_modem_checker'),
    path('api/get-form-data-signal-checker/', FormDataSignalChecker.as_view(), name='get_form_data_signal_checker'),
    path('api/get-form-data-server-checker/', FormDataServerChecker.as_view(), name='get_form_data_server_checker'),

    path('api/get-form-data-setting-modbus/', FormModbusView.as_view(), name='get_form_data_setting_modbus'),
    path('api/get-form-data-limitation/', FormDataLimitation.as_view(), name='get_form_data_limitation'),
    path('api/get-form-data-compensation/', FormDataCompensation.as_view(), name='get_form_data_compensation'),
    path('api/get-form-data-setting-log/', FormDataSettingLogs.as_view(), name='get_form_data_setting_log'),

    path('api/get-form-database/', FormDataBasePropierties.as_view(), name='get_form_data_base'),
    path('api/checkPassword/',CheckPassword.as_view(),name='post_check_password'),
    path('api/changePassword/',ChangePassword.as_view(),name='put_change_password'),
    path("api/colecciones/", ListColections.as_view(), name="list_colections"),
    path("api/modem/", ModemView.as_view(), name="modem"),
    path('interface-1/', InterfaceConnection.as_view(), {'connection_name': 'Wired connection 1'},name="connection_one"),
    path('interface-2/', InterfaceConnection.as_view(), {'connection_name': 'Wired connection 2'},name="connection_two"),
    path('api/antenna-wifi/', AntennaWifi.as_view(),name="antenna_wifi"),
    path('api/add-wifi/', AddWifi.as_view(),name="add_wifi"),
    path('api/modbus/view-devices/',FormModbusDevicesView.as_view(),name='view_devices'),
    path('api/modbus/add-device-rtu/',FormModbusAddDeviceRtu.as_view(),name='add_rtu'),
    path('api/modbus/add-device-tcp/',FormModbusAddDeviceTcp.as_view(),name='add_tcp'),
    path('api/modbus/modify-device-tcp/',FormModbusDeviceRtuView.as_view(),name='modify_device_rtu'),

    path('api/modbus/view-devices-add/',FormModbusGetDevicesView.as_view(),name='view_devices_add'),
    path('api/delete/database/',DeleteCollectionView.as_view(),name='delete_database'),
    path('api/delete/log/',DeleteLog.as_view(),name='delete_log')

]