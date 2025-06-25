module.exports = {
  root: true,
  env: { node: true },
  extends: [
    'plugin:vue/vue3-recommended',
    'eslint:recommended',
    '@vue/typescript/recommended'
  ],
  parserOptions: {
    ecmaVersion: 2020
  },
  rules: {
    // Add custom rules here if needed
  }
} 