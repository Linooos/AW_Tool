#pragma once
#define WIN32_LEAN_AND_MEAN

#include <string>
#include <vector>
#include <wbemidl.h>
#include <wtypes.h>
#include <comutil.h>
#include <comdef.h>
#include<unordered_map>

struct BIOSEnumerationAttributes {
	BSTR AttributeName;
	BSTR CurrentValue;
	BSTR DisplayName ;
	BSTR DefaultValue;
	std::vector<BSTR> possible;
};
struct OptionNames {
	BSTR showName;
	BSTR attrName;
};
struct BIOSIntegerAttribute {
	BSTR AttributeName;
	BSTR DisplayName;
	DWORD CurrentValue;
	DWORD DefaultValue;
	DWORD LowerBound;
	DWORD UpperBound;
};

struct BIOSStringAttribute {
	BSTR AttributeName;
	BSTR DisplayName;
	BSTR CurrentValue;
	DWORD MaxLength;
	DWORD MinLength;
};

struct BIOSCOLLECTION {
	BSTR AttributeName;
	BSTR DisplayName;
	DWORD Count;
	std::vector<BSTR> atrr;
};

namespace BiosContrl {
	class BiosContrl_SDK
	{
	public:
		//bool isBiosPwd();//p
		//int unlockBios();//p
		static BiosContrl_SDK* getInstance();

		DWORD setSingleConfig(BSTR option, BSTR value);
		DWORD setSingleConfigByIndex(DWORD index, BSTR value);
		DWORD showOptionList();
		
		BiosContrl_SDK();
		~BiosContrl_SDK();
		std::vector<BIOSEnumerationAttributes> attributes ;
		std::vector<BIOSIntegerAttribute>integers;
		std::vector<BIOSStringAttribute>strings;
		std::vector<OptionNames> LOptionsName;
		//std::unordered_map<PSTR, PSTR> mapName;
	private:
		DWORD loadBios();
		
		IWbemLocator* m_WbemLocator = NULL;
		IWbemServices* m_WbemBios =NULL;
		IEnumWbemClassObject* m_WbemBIOSAttributeInterface = NULL;
		IEnumWbemClassObject* m_WbemBIOSEnumerationAttributes = NULL;
		IEnumWbemClassObject* m_WbemBIOSIntegerAttributes = NULL;
		IEnumWbemClassObject* m_WbemBIOSStringAttributes = NULL;
		IWbemClassObject* m_WbemBIOSInterfaces = NULL;
		bool isKeyset;
		int inital();
		BSTR getStringTypeOption(IWbemClassObject* wmi , LPCWSTR str1);
		std::vector<BSTR> getVectorOption(IWbemClassObject* wmi, LPCWSTR str1);
		DWORD getDwordOption(IWbemClassObject* wmi, LPCWSTR str1);
	};
}



