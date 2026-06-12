#ifndef TO_WSTRING_EXT_H
#define TO_WSTRING_EXT_H

#include <string>
#include <codecvt>
#include <locale>

// Explicitly extending the std namespace
namespace std {

    inline std::wstring to_wstring(const std::string& str) {

        int wideLen = MultiByteToWideChar(CP_UTF8, 0, str.c_str(), -1, NULL, 0);
        
        if (wideLen > 0) {
            // 2. Allocate the wide string buffer
            std::wstring wide_str(wideLen - 1, L'\0'); 
            
            // 3. Perform the actual conversion
            MultiByteToWideChar(CP_UTF8, 0, str.c_str(), -1, &wide_str[0], wideLen);
            
            return wide_str;
        } else {
            return L"";
        }
        
    }

}

#endif // TO_WSTRING_EXT_H
