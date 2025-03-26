from django.contrib import admin
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView) 
from django.urls import path
from AppFrontend.Views.checkPassWordView import ChangePassword, CheckPassword
from AppFrontend.Views.contenView import ContentView, ContentViewMenuChecker, ContentViewMenuCompensationLimitation, ContentViewMenuDatabase, ContentViewMenuMain, ContentViewMenuModbus, ContentViewMenuSetting, ContentViewSingleDevice
from AppFrontend.Views.deleteView import DeleteCollectionView,DeleteLog
from AppFrontend.Views.homeView import HomeView
from AppFrontend.Views.settingSystemView import AddWifi, AntennaWifi, InterfaceConnection
from AppFrontend.Views.jsonView import ListColections
from AppFrontend.Views.logView import DownloadLogsView, GetLogSingleDeviceView, GetLogsView
from AppFrontend.Views.loginView import IndexView
from AppFrontend.Views.menuView import FormDataBasePropierties, FormDataCompensation, FormDataLimitation, FormDataModemChecker, FormDataModes, FormDataServer, FormDataServerChecker, FormDataSettingDataBase, FormDataSettingInterface, FormDataSettingLogs, FormDataSignalChecker, MeasureView
from AppFrontend.Views.modbusView import FormModbusAddDeviceRtu, FormModbusAddDeviceTcp, FormModbusDeviceRtuView, FormModbusDevicesView, FormModbusGetDevicesView, FormModbusView
from AppFrontend.Views.modemView import ModemView
from AppFrontend.Views.singleDeviceView import FormModbusReadRtu, FormModbusReadTCP
from AppFrontend.Views.whiteListView import DeleteWhiteList, ModemManager
from authApp.views.userDetailView import UserDetailView
from energyAPP.views.inverterDataView import InverterApiView, InverterDataView, InverterView
from energyAPP.views.serviceView import Reboot, StartView, StatusService, StopView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('home/content/<str:option>/', ContentView.as_view(), name='get_content'),
    path('home/content/form/<str:option>/', ContentViewMenuMain.as_view(), name='get_main_menu_content'),
    path('home/content/form/modbus/<str:option>/', ContentViewMenuModbus.as_view(), name='get_modbus_menu_content'),
    path('home/content/form/compensation-limitation/<str:option>/', ContentViewMenuCompensationLimitation.as_view(), name='get_content_form_compensation-limitation'),
    path('home/content/form/database/<str:option>/', ContentViewMenuDatabase.as_view(), name='get_database_menu_content'),
    path('home/content/form/checker/<str:option>/', ContentViewMenuChecker.as_view(), name='get_checker_menu_content'),
    path('home/content/form/setting/<str:option>/', ContentViewMenuSetting.as_view(), name='get_settings_menu_content'),
    path('home/content/form/read_rtu_tcp/<str:option>/',ContentViewSingleDevice.as_view(), name='get_content_Single_device'),
    path('user/', UserDetailView.as_view(), name='user'),
    path('user/<str:user_id>/', UserDetailView.as_view(), name='user_detail'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/inverter-data/', InverterDataView.as_view(), name='inverter_data'),
    path('home/start/', StartView.as_view(), name='start_service'),
    path('home/stop/', StopView.as_view(), name='stop_service'),
    path('home/reboot/', Reboot.as_view(), name='reboot_erco_pulse'),
    path('home/status/', StatusService.as_view(), name='status_service'),

    # path("home/logs/", LogTemplateView.as_view(), name="log_view"),
    path("home/api/logs/", GetLogsView.as_view(), name="fetch_logs"),
    path("home/api/log/singleDevice/", GetLogSingleDeviceView.as_view(),name="log_single_device"),
    path("home/api/logs/download/",DownloadLogsView.as_view(),name="download_logs"),
    path('api/measurement/', MeasureView.as_view(), name='get_measurement_data'),
    path('api/server/config/', FormDataServer.as_view(), name='get_server_config'),
    path('api/modes/config/', FormDataModes.as_view(), name='get_modes_config'),
    path('api/settings/database/', FormDataSettingDataBase.as_view(), name='get_database_settings'),
    path('api/settings/interface/', FormDataSettingInterface.as_view(), name='get_interface_settings'),
    path('api/status/modem/', FormDataModemChecker.as_view(), name='get_modem_status'),
    path('api/status/signal/', FormDataSignalChecker.as_view(), name='get_signal_status'),
    path('api/status/server/', FormDataServerChecker.as_view(), name='get_server_status'),

    path('api/settings/modbus/', FormModbusView.as_view(), name='get_modbus_settings'),
    path('api/config/limitation/', FormDataLimitation.as_view(), name='get_limitation_config'),
    path('api/config/compensation/', FormDataCompensation.as_view(), name='get_compensation_config'),
    path('api/settings/logs/', FormDataSettingLogs.as_view(), name='get_log_settings'),

    path('api/database/config/', FormDataBasePropierties.as_view(), name='get_database_config'),
    path('api/password/verify/',CheckPassword.as_view(),name='verify_password'),
    path('api/password/change/',ChangePassword.as_view(),name='change_password'),
    path('api/collections/', ListColections.as_view(), name="list_colections"),
    path('api/modem/status/', ModemView.as_view(), name="modem_status"),
    path('network/interface-1/', InterfaceConnection.as_view(), {'connection_name': 'Wired connection 1'},name="connection_one"),
    path('network/interface-2/', InterfaceConnection.as_view(), {'connection_name': 'Wired connection 2'},name="connection_two"),
    path('network/wifi/toggle/', AntennaWifi.as_view(),name="toggle_wifi"),
    path('network/wifi/add/', AddWifi.as_view(),name="add_wifi"),
    path('api/modbus/devices/',FormModbusDevicesView.as_view(),name='modbus_devices_list'),
    path('api/modbus/device/add-rtu/',FormModbusAddDeviceRtu.as_view(),name='add_modbus_device_rtu'),
    path('api/modbus/device/add-tcp/',FormModbusAddDeviceTcp.as_view(),name='add_modbus_device_tcp'),
    path('api/modbus/device/modify-rtu/',FormModbusDeviceRtuView.as_view(),name='modify_modbus_device_rtu'),
    path('api/modbus/devices/detail/',FormModbusGetDevicesView.as_view(),name='modbus_devices_detail'),
    path('api/database/delete/',DeleteCollectionView.as_view(),name='delete_database'),
    path('api/logs/delete/',DeleteLog.as_view(),name='delete_log'),
    path('api/inverter/status/',InverterView.as_view(), name='inverter_status'),
    path('api/inverter/export/', InverterApiView.as_view(), name='export_inverter_data'),
    path('api/setting/whitelist/',DeleteWhiteList.as_view(),name='view_list'),
    path('api/setting/modemManager/',ModemManager.as_view(),name='modem_manager'),
    
    path('api/read/rtu/',FormModbusReadRtu.as_view(),name='rtu_single_device'),
    path('api/read/tcp/',FormModbusReadTCP.as_view(),name='tcp_single_device')

]