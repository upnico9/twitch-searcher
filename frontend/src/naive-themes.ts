// src/naive-theme.ts
import { darkTheme } from 'naive-ui'
import type { GlobalThemeOverrides } from 'naive-ui'

export const theme = darkTheme

export const themeOverrides: GlobalThemeOverrides = {
  common: {
    primaryColor: '#9147ff',
    primaryColorHover: '#a970ff',
    primaryColorPressed: '#772ce8',
    primaryColorSuppl: '#b881ff',
  },
  Button: {
    textColor: '#fff',
    colorPrimary: '#9147ff',
    colorHoverPrimary: '#a970ff',
    colorPressedPrimary: '#772ce8',
  },
  Card: {
    color: '#262626',
    textColor: '#ffffff',
    titleTextColor: '#ffffff',
  },
  Input: {
    color: '#1f1f23',
    textColor: '#ffffff',
    placeholderColor: '#aaaaaa',
    borderColor: '#333333',
  },
  Select: {
    peers: {
      InternalSelection: {
        color: '#1f1f23',
        textColor: '#ffffff',
        placeholderColor: '#aaaaaa',
      },
    },
  },
}
