{
  'includes': [ 'common.gypi' ],
  'variables': {
      'std%':'ansi',
      "module_name":"<!(node -e \"console.log(require('./package.json').binary.module_name)\")",
      "module_path":"<!(node -e \"console.log(require('./package.json').binary.module_path)\")",
  },
  'targets': [
    {
      'target_name': '<(module_name)',
      'include_dirs': [
          "<!(node -e \"require('nan')\")",
          '<!@(pkg-config libosrm --variable=includedir)',
          './src/'
      ],
      'libraries': [
        '<!@(pkg-config libosrm --libs --static)'
      ],
      'defines': ['LIBOSRM_GIT_REVISION="<!@(pkg-config libosrm --modversion)"'],
      'conditions': [
        [ 'OS=="linux"', {
          # remove the older style c++11 flag
          # inherited by node >= 4.x
          'cflags_cc!' : [
              '-std=gnu++0x'
          ],
          'cflags_cc' : [
              '-std=c++1y', # to support gcc 4.8: https://github.com/Project-OSRM/osrm-backend/pull/2805
              '<!@(pkg-config libosrm --cflags)'
          ],
          'libraries':[
              '-Wl,-rpath=<!@(pkg-config libosrm --variable=libdir)',
              '-lboost_program_options',
              '-lboost_regex'
          ]}
        ],
        ['OS=="mac"', {
          'xcode_settings': {
            'CLANG_CXX_LIBRARY': 'libc++',
            'CLANG_CXX_LANGUAGE_STANDARD':'c++14',
            'GCC_VERSION': 'com.apple.compilers.llvm.clang.1_0',
            'MACOSX_DEPLOYMENT_TARGET':'10.8',
            'OTHER_LDFLAGS':[
              '-Wl,-bind_at_load'
            ]
          }
        }
        ]
      ],
      'sources': [
        "src/node_osrm.cpp"
      ],
      'cflags_cc!': ['-fno-rtti', '-fno-exceptions'],
      'xcode_settings': {
        'OTHER_CPLUSPLUSFLAGS':['-Wno-unneeded-internal-declaration', '-Wno-unknown-pragmas', '<!@(pkg-config libosrm --cflags)'],
        'GCC_ENABLE_CPP_RTTI': 'YES',
        'GCC_ENABLE_CPP_EXCEPTIONS': 'YES'
      }
    },
    {
      'target_name': 'action_after_build',
      'type': 'none',
      'dependencies': [ '<(module_name)' ],
      'copies': [
          {
            'files': [ '<(PRODUCT_DIR)/<(module_name).node' ],
            'destination': '<(module_path)'
          }
      ]
    }
  ]
}
