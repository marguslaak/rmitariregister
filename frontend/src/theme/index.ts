import { extendTheme } from '@chakra-ui/react';

const overrides = {
  borderRadius: {
    sm: '2px',
    base: '4px',
    md: '16px',
    lg: '20px',
  },
  letterSpacings: {
    wide: '0.01em',
    wider: '0.04em',
    widest: '3px',
  },
  sizes: {
    '7xl': '80rem',
    '8xl': '88rem',
    '9xl': '96rem',
  },
  styles: {
    global: {
      body: {
        overflowX: 'hidden',
        fontSize: 'md',
        lineHeight: 'base',
      },
    },
  },
};
const customTheme = extendTheme(overrides);
export default customTheme;
