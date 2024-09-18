#include "BiosControl.h"
#include <iostream>

#pragma comment(lib, "wbemuuid.lib")
// #pragma comment(lib, "comsuppwd.lib")

// #define _DEBUG
DWORD BiosContrl::BiosContrl_SDK::loadBios()
{
	if (isKeyset == TRUE)
	{
	}

	IWbemClassObject *m_EnumAttr = NULL;
	ULONG uReturn = 0;
	// ѭ�����е���ʵ��
	while (m_WbemBIOSEnumerationAttributes)
	{
		m_WbemBIOSEnumerationAttributes->Next(WBEM_INFINITE, 1, &m_EnumAttr, &uReturn);
		if (0 == uReturn)
			break;

		BSTR attrnameStr = getStringTypeOption(m_EnumAttr, L"AttributeName");
		BSTR defaultValue = getStringTypeOption(m_EnumAttr, L"DefaultValue");
		BSTR displayName = getStringTypeOption(m_EnumAttr, L"DisplayName");
		BSTR currentValue = getStringTypeOption(m_EnumAttr, L"CurrentValue");
		std::vector<BSTR> lpossible = getVectorOption(m_EnumAttr, L"PossibleValue");
#ifdef _DEBUG
		std::wcout << L"D: " << displayName << std::endl;
#endif
		attributes.push_back(BIOSEnumerationAttributes{attrnameStr, currentValue, displayName, defaultValue, lpossible});
		m_EnumAttr->Release();
	}
	while (m_WbemBIOSIntegerAttributes)
	{
		m_WbemBIOSIntegerAttributes->Next(WBEM_INFINITE, 1, &m_EnumAttr, &uReturn);
		if (0 == uReturn)
			break;
		BSTR attrnameStr = getStringTypeOption(m_EnumAttr, L"AttributeName");
		DWORD defaultValue = getDwordOption(m_EnumAttr, L"DefaultValue");
		BSTR displayName = getStringTypeOption(m_EnumAttr, L"DisplayName");
		DWORD currentValue = getDwordOption(m_EnumAttr, L"CurrentValue");
		DWORD lowerBound = getDwordOption(m_EnumAttr, L"LowerBound");
		DWORD upperBound = getDwordOption(m_EnumAttr, L"UpperBound");
#ifdef _DEBUG
		std::wcout << L"D: " << displayName << std::endl;
#endif
		integers.push_back(BIOSIntegerAttribute{attrnameStr, displayName, currentValue, defaultValue, lowerBound, upperBound});
		m_EnumAttr->Release();
	}
	while (m_WbemBIOSStringAttributes)
	{
		m_WbemBIOSStringAttributes->Next(WBEM_INFINITE, 1, &m_EnumAttr, &uReturn);
		if (0 == uReturn)
			break;
		BSTR attrnameStr = getStringTypeOption(m_EnumAttr, L"AttributeName");
		BSTR displayName = getStringTypeOption(m_EnumAttr, L"DisplayName");
		BSTR defaultValue = getStringTypeOption(m_EnumAttr, L"DefaultValue");
		DWORD maxLength = getDwordOption(m_EnumAttr, L"MaxLength");
		DWORD minLength = getDwordOption(m_EnumAttr, L"MinLength");

#ifdef _DEBUG
		std::wcout << L"D: " << displayName << std::endl;
#endif
		strings.push_back(BIOSStringAttribute{attrnameStr, displayName, defaultValue, maxLength, minLength});
		m_EnumAttr->Release();
	}
	// ����Index�б�
	for (const auto &attr : attributes)
	{
		LOptionsName.push_back(OptionNames{attr.DisplayName, attr.AttributeName});
	}
	for (const auto &attr : strings)
	{
		LOptionsName.push_back(OptionNames{attr.DisplayName, attr.AttributeName});
	}
	for (const auto &attr : integers)
	{
		LOptionsName.push_back(OptionNames{attr.DisplayName, attr.AttributeName});
	}
	return 0;
}
BiosContrl::BiosContrl_SDK* BiosContrl::BiosContrl_SDK::getInstance()
{
	return new BiosContrl_SDK();
}
DWORD BiosContrl::BiosContrl_SDK::setSingleConfig(BSTR option, BSTR value)
{
	// ����setattribute�������ڵ���ʵ��
	IEnumWbemClassObject *enum_obj; // ö�ٶ������ʱ����
	VARIANT path;					// ����·��
	if (m_WbemBios->CreateInstanceEnum((BSTR)L"BIOSAttributeInterface", WBEM_FLAG_FORWARD_ONLY, NULL, &enum_obj) == S_OK)
	{
		std::cout << "path runing";
		IWbemClassObject *spInstance;
		ULONG uNumOfInstances = 0;
		enum_obj->Next(10000, 1, &spInstance, &uNumOfInstances);
		spInstance->Get((BSTR)L"__Path", 0, &path, 0, 0);
		spInstance->Release();
		enum_obj->Release();
	}
	else
	{
#ifdef _DEBUG
		printf("pathError: OK\n");
#endif
		return -1;
	}
	enum_obj->Release();

	// ��ʼ������
	IWbemClassObject *pInParamsDefinition = NULL;
	std::cout << m_WbemBIOSInterfaces->GetMethod((BSTR)L"setAttribute", 0, &pInParamsDefinition, NULL);

	IWbemClassObject *pInParams = NULL;
	pInParamsDefinition->SpawnInstance(0, &pInParams);
	//////////////////////////////////////////////////////////////////////////////////////////////////////////
	VARIANT param1{VT_I4};
	param1.uintVal = 1; // ��ʱռλ
	pInParams->Put((BSTR)L"SecType", NULL, &param1, 0);

	/////////////////////////////////////////////////////////////////////////////////////////////////////////
	VARIANT param2{VT_I4};
	param2.uintVal = 0; // ��ʱռλ
	pInParams->Put((BSTR)L"SecHndCount", NULL, &param2, 0);

	////////////////////////////////////////////////////////////////////////////////////////////////////////
	std::vector<int8_t> myVector = {};
	VARIANT param3{VT_ARRAY | VT_I1};
	SAFEARRAYBOUND sa = {myVector.size(), 0};
	SAFEARRAY *psa = SafeArrayCreate(VT_UI1, 1, &sa);

	void *pArrayData = NULL;
	SafeArrayAccessData(psa, &pArrayData);
	memcpy(pArrayData, myVector.data(), myVector.size());
	SafeArrayUnaccessData(psa);
	param3.parray = psa;
	pInParams->Put((BSTR)L"SecHandle", NULL, &param3, 0);

	///////////////////////////////////////////////////////////////////////////////////////////////////////
	VARIANT param4{VT_BSTR};
	param4.bstrVal = SysAllocString(option);
	pInParams->Put((BSTR)L"AttributeName", NULL, &param4, 0);

	VARIANT param5{VT_BSTR};
	param5.bstrVal = SysAllocString(value);
	pInParams->Put((BSTR)L"AttributeValue", NULL, &param5, 0);

	// ���з���
	VARIANT result{VT_I4};
	result.intVal = -1;
	IWbemClassObject *pOutParams = NULL;
	if ((m_WbemBios->ExecMethod((BSTR)path.bstrVal, (BSTR)L"SetAttribute", 0, NULL, pInParams, &pOutParams, NULL)) == S_OK)
	{
#ifdef _DEBUG
		printf("res method: OK\n");
#endif
		pOutParams->Get((BSTR)L"Status", 0, &result, nullptr, nullptr);
		pOutParams->Release();
		VariantClear(&param1);
		VariantClear(&param2);
		VariantClear(&param3);
		VariantClear(&param4);
		VariantClear(&param5);
		return result.intVal;
	}
	VariantClear(&param1);
	VariantClear(&param2);
	VariantClear(&param3);
	VariantClear(&param4);
	VariantClear(&param5);
	return -1;
}
DWORD BiosContrl::BiosContrl_SDK::setSingleConfigByIndex(DWORD index, BSTR value)
{
	index = index < 0 ? 0 : index;
	index = index <= LOptionsName.size() - 1 ? index : LOptionsName.size() - 1;
	return setSingleConfig(LOptionsName[index].attrName, value);
}
DWORD BiosContrl::BiosContrl_SDK::showOptionList()
{
	DWORD index = 0;
	for (const auto &attr : LOptionsName)
	{
		std::wcout << index << " : " << attr.showName << "\n";
		index++;
	}
	return 0;
}
BiosContrl::BiosContrl_SDK::BiosContrl_SDK()
{
	// ��ʼ��WMI�߳�
	IWbemLocator *m_WbemLocator;
	CoInitializeEx(nullptr, COINIT::COINIT_MULTITHREADED);
	CoInitializeSecurity(nullptr, -1, nullptr, nullptr,
						 RPC_C_AUTHN_LEVEL_NONE, // RPC_C_AUTHN_LEVEL_CONNECT,
						 RPC_C_IMP_LEVEL_IMPERSONATE,
						 nullptr, EOAC_NONE, nullptr);
	CoCreateInstance(CLSID_WbemLocator, nullptr, CLSCTX_INPROC_SERVER, IID_IWbemLocator, (void **)&m_WbemLocator);
	// ��ָ��dell bios��·����

	m_WbemLocator->ConnectServer((BSTR)L"ROOT\\dcim\\sysman\\biosattributes", nullptr, nullptr, nullptr, NULL, nullptr, nullptr, &m_WbemBios);
	m_WbemLocator->Release();

	inital();
}
int BiosContrl::BiosContrl_SDK::inital()
{
	// ע��biosѡ���ȡWMI
	if (m_WbemBios->ExecQuery(bstr_t("WQL"), bstr_t("SELECT * FROM EnumerationAttribute"), WBEM_FLAG_FORWARD_ONLY | WBEM_FLAG_RETURN_IMMEDIATELY, NULL, &m_WbemBIOSEnumerationAttributes) == S_OK)
	{
#ifdef _DEBUG
		printf("EnumerationAttributes OK\n");
#endif
	}
	else
	{
		return -1;
	}

	if (m_WbemBios->ExecQuery(bstr_t("WQL"), bstr_t("SELECT * FROM IntegerAttribute"), WBEM_FLAG_FORWARD_ONLY | WBEM_FLAG_RETURN_IMMEDIATELY, NULL, &m_WbemBIOSIntegerAttributes) == S_OK)
	{
#ifdef _DEBUG
		printf("IntegerAttribute OK\n");
#endif
	}
	else
	{
		return -1;
	}

	if (m_WbemBios->ExecQuery(bstr_t("WQL"), bstr_t("SELECT * FROM StringAttribute"), WBEM_FLAG_FORWARD_ONLY | WBEM_FLAG_RETURN_IMMEDIATELY, NULL, &m_WbemBIOSStringAttributes) == S_OK)
	{
#ifdef _DEBUG
		printf("StringAttribute OK\n");
#endif
	}
	else
	{
		return -1;
	}

	if (m_WbemBios->GetObject((BSTR)L"BIOSAttributeInterface", NULL, nullptr, &m_WbemBIOSInterfaces, nullptr) == S_OK)
	{
#ifdef _DEBUG
		printf("Interface OK\n");
#endif
	}
	else
	{
		return -1;
	}

	loadBios();
	return 0;
}
BiosContrl::BiosContrl_SDK::~BiosContrl_SDK()
{
	// �ͷ��߳�
	if (m_WbemBios)
		m_WbemBios->Release();
	if (m_WbemBIOSAttributeInterface)
		m_WbemBIOSAttributeInterface->Release();
	if (m_WbemBIOSEnumerationAttributes)
		m_WbemBIOSEnumerationAttributes->Release();
	if (m_WbemBIOSIntegerAttributes)
		m_WbemBIOSIntegerAttributes->Release();
	if (m_WbemBIOSStringAttributes)
		m_WbemBIOSStringAttributes->Release();

	CoUninitialize();
	if (!attributes.empty())
	{
		for (auto &attr : attributes)
		{
			SysFreeString(attr.AttributeName);
			SysFreeString(attr.CurrentValue);
			SysFreeString(attr.DefaultValue);
			SysFreeString(attr.DisplayName);
			for (const auto &poss : attr.possible)
			{
				SysFreeString(poss);
			}
		}
	}
	if (!integers.empty())
	{
		for (auto &attr : integers)
		{
			SysFreeString(attr.AttributeName);
			SysFreeString(attr.DisplayName);
		}
	}
	if (!integers.empty())
	{
		for (auto &attr : strings)
		{
			SysFreeString(attr.AttributeName);
			SysFreeString(attr.DisplayName);
			SysFreeString(attr.CurrentValue);
		}
	}
}
BSTR BiosContrl::BiosContrl_SDK::getStringTypeOption(IWbemClassObject *wmi, LPCWSTR str1)
{
	VARIANT vtProp;
	// ��ȡAttributeName
	wmi->Get(str1, 0, &vtProp, 0, 0);
	BSTR str = SysAllocString(vtProp.bstrVal);
	VariantClear(&vtProp);
#ifdef _DEBUG
	std::wcout << L"A: " << str << std::endl;
#endif
	return str;
}
DWORD BiosContrl::BiosContrl_SDK::getDwordOption(IWbemClassObject *wmi, LPCWSTR str1)
{
	VARIANT vtProp;
	// ��ȡAttributeName
	wmi->Get(str1, 0, &vtProp, 0, 0);
	DWORD temp = V_I4(&vtProp);
	VariantClear(&vtProp);
#ifdef _DEBUG
	std::wcout << L"A: " << temp << std::endl;
#endif
	return temp;
}
std::vector<BSTR> BiosContrl::BiosContrl_SDK::getVectorOption(IWbemClassObject *wmi, LPCWSTR str1)
{
	VARIANT vtProp;
	wmi->Get(str1, 0, &vtProp, 0, 0);
	std::vector<BSTR> lpossible;
	if (V_VT(&vtProp) == (VT_ARRAY | VT_BSTR))
	{
		SAFEARRAY *psa = V_ARRAY(&vtProp);
		BSTR *pData;

		// ��ȡSAFEARRAY������
		if (SUCCEEDED(SafeArrayAccessData(psa, (void **)&pData)))
		{
			// ��ȡ����Ĵ�С
			long lowerBound, upperBound;
			SafeArrayGetLBound(psa, 1, &lowerBound);
			SafeArrayGetUBound(psa, 1, &upperBound);
			long count = upperBound - lowerBound + 1;

			// ��������
			for (long i = 0; i < count; ++i)
			{
				lpossible.push_back(SysAllocString(pData[i]));
#ifdef _DEBUG
				std::wcout << L"possible: " << pData[i] << std::endl;
#endif
			}

			// ������Ϻ���Ҫ�����SAFEARRAY�ķ���
			SafeArrayUnaccessData(psa);
		}
	}
	VariantClear(&vtProp);
	return lpossible;
}
