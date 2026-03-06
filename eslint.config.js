export default [
  {
    ignores: [
      'dist',
      'node_modules',
      'coverage',
      '**/*.ts',
      '**/*.tsx',
      'tailwind.config.ts',
      'vite.config.ts'
    ]
  },
  {
    files: ['**/*.{js,mjs,cjs}'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module'
    }
  }
];
