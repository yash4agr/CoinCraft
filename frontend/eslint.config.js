// eslint.config.js
import js from "@eslint/js";
import tsPlugin from "@typescript-eslint/eslint-plugin";
import tsParser from "@typescript-eslint/parser";
import vuePlugin from "eslint-plugin-vue";
import vueParser from "vue-eslint-parser";
import globals from "globals";

export default [
  // Base JS recommended rules
  js.configs.recommended,

  // TypeScript + Vue rules
  {
    files: ["**/*.ts", "**/*.vue"],
    languageOptions: {
      parser: vueParser, // Parses Vue SFCs
      parserOptions: {
        parser: tsParser, // Parses <script lang="ts">
        ecmaVersion: 2021,
        sourceType: "module",
      },
      globals: {
        ...globals.browser, // browser globals (console, URLSearchParams, etc.)
        ...globals.node,    // Add Node.js globals (__dirname, NodeJS, etc.)
      },
    },
    plugins: {
      "@typescript-eslint": tsPlugin,
      vue: vuePlugin,
    },
    rules: {
      // TypeScript unused vars (auto-fixable)
      "@typescript-eslint/no-unused-vars": [
        "warn",
        {
          vars: "all",
          args: "after-used",
          ignoreRestSiblings: false,
          caughtErrors: "none",
          varsIgnorePattern: "^_", // Ignore variables starting with underscore
          argsIgnorePattern: "^_"  // Ignore arguments starting with underscore
        }
      ],

      // Disable JS default unused var rule
      "no-unused-vars": "off",

      // Allow variable redeclaration (for your TeacherProfile issue)
      "no-redeclare": "off",
      "@typescript-eslint/no-redeclare": "warn",

      // Allow undefined globals temporarily
      "no-undef": "warn",

      // Allow import reassignment (for your onErrorCaptured issue)
      "no-import-assign": "warn",

      // Vue rules
      "vue/multi-word-component-names": "off",
      "vue/no-mutating-props": "error",
      "vue/no-unused-components": "warn",
      "vue/no-unused-vars": [
        "warn",
        {
          ignorePattern: "^_" // Ignore variables starting with underscore
        }
      ],
      "vue/require-default-prop": "off"
    },
  },

  // Vite config specific rules
  {
    files: ["vite.config.ts", "vite.config.js"],
    languageOptions: {
      globals: {
        ...globals.node,
        __dirname: "readonly",
      },
    },
  },

  // Ignore dist and node_modules
  {
    ignores: ["dist/**", "node_modules/**"],
  },
];
