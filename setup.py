from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import platform


class BuildExt(build_ext):
    def get_source_files(self):
        filenames = build_ext.get_source_files(self)
        for ext in self.extensions:
            filenames.extend(ext.depends)
        return filenames

    def build_extension(self, ext):
        c_sources = []
        cxx_sources = []
        for source in ext.sources:
            if source.endswith(".c"):
                c_sources.append(source)
            else:
                cxx_sources.append(source)
        extra_args = ext.extra_compile_args or []

        objects = []
        for lang, sources in (("c", c_sources), ("c++", cxx_sources)):
            if lang == "c++": 
                if self.compiler.compiler_type in ["unix", "cygwin", "mingw32"]:
                    extra_args.append("-std=c++0x")
                elif self.compiler.compiler_type == "msvc":
                    extra_args.append("/EHsc")

            macros = ext.define_macros[:]
            if platform.system() == "Darwin":
                macros.append(("OS_MACOSX", "1"))
            for undef in ext.undef_macros:
                macros.append((undef,))

            objs = self.compiler.compile(sources,
                                         output_dir=self.build_temp,
                                         macros=macros,
                                         include_dirs=ext.include_dirs,
                                         debug=self.debug,
                                         extra_postargs=extra_args,
                                         depends=ext.depends)
            objects.extend(objs)

        self._built_objects = objects[:]
        if ext.extra_objects:
            objects.extend(ext.extra_objects)
        extra_args = ext.extra_link_args or []

        ext_path = self.get_ext_fullpath(ext.name)
        # Detect target language, if not provided
        language = ext.language or self.compiler.detect_language(sources)

        self.compiler.link_shared_object(
            objects, ext_path,
            libraries=self.get_libraries(ext),
            library_dirs=ext.library_dirs,
            runtime_library_dirs=ext.runtime_library_dirs,
            extra_postargs=extra_args,
            export_symbols=self.get_export_symbols(ext),
            debug=self.debug,
            build_temp=self.build_temp,
            target_lang=language)

brotli = Extension("brotli",
                    sources=[
                        "brotli/python/brotlimodule.cc",
                        "brotli/enc/backward_references.cc",
                        "brotli/enc/block_splitter.cc",
                        "brotli/enc/brotli_bit_stream.cc",
                        "brotli/enc/encode.cc",
                        "brotli/enc/entropy_encode.cc",
                        "brotli/enc/histogram.cc",
                        "brotli/enc/literal_cost.cc",
                        "brotli/dec/bit_reader.c",
                        "brotli/dec/decode.c",
                        "brotli/dec/huffman.c",
                        "brotli/dec/safe_malloc.c",
                        "brotli/dec/streams.c",
                        "brotli/dec/state.c",
                    ],
                    depends=[
                        "brotli/enc/backward_references.h",
                        "brotli/enc/bit_cost.h",
                        "brotli/enc/block_splitter.h",
                        "brotli/enc/brotli_bit_stream.h",
                        "brotli/enc/cluster.h",
                        "brotli/enc/command.h",
                        "brotli/enc/context.h",
                        "brotli/enc/dictionary.h",
                        "brotli/enc/encode.h",
                        "brotli/enc/entropy_encode.h",
                        "brotli/enc/fast_log.h",
                        "brotli/enc/find_match_length.h",
                        "brotli/enc/hash.h",
                        "brotli/enc/histogram.h",
                        "brotli/enc/literal_cost.h",
                        "brotli/enc/port.h",
                        "brotli/enc/prefix.h",
                        "brotli/enc/ringbuffer.h",
                        "brotli/enc/static_dict.h",
                        "brotli/enc/transform.h",
                        "brotli/enc/write_bits.h",
                        "brotli/dec/bit_reader.h",
                        "brotli/dec/context.h",
                        "brotli/dec/decode.h",
                        "brotli/dec/dictionary.h",
                        "brotli/dec/huffman.h",
                        "brotli/dec/prefix.h",
                        "brotli/dec/safe_malloc.h",
                        "brotli/dec/streams.h",
                        "brotli/dec/transform.h",
                        "brotli/dec/types.h",
                        "brotli/dec/state.h",
                    ],
                    language="c++",
                    )

setup(
    name="Brotli",
    version="0.1",
    url="https://github.com/google/brotli",
    description="Python binding of the Brotli compression library",
    author="Khaled Hosny",
    author_email="khaledhosny@eglug.org",
    license="Apache 2.0",
    ext_modules=[brotli],
    cmdclass={'build_ext': BuildExt},
)
