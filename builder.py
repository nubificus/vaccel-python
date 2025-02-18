from cffi import FFI


ffibuilder = FFI()

ffibuilder.set_source(
    "vaccel._vaccel",
    r"""
        #include <vaccel.h>
        """,
    libraries=['vaccel-python', 'dl'],
)

ffibuilder.cdef("""
        typedef enum {
                VACCEL_RESOURCE_LIB = 0,
                VACCEL_RESOURCE_DATA,
                VACCEL_RESOURCE_MODEL,
                VACCEL_RESOURCE_MAX
        } vaccel_resource_type_t;
                
        typedef enum {
                VACCEL_PATH_LOCAL_FILE = 0,
                VACCEL_PATH_LOCAL_DIR,
                VACCEL_PATH_REMOTE_FILE,
                VACCEL_PATH_MAX
        } vaccel_path_type_t;
        """
        )

# Session API
ffibuilder.cdef("""
        typedef int64_t vaccel_id_t;
        
        struct vaccel_session {
                /* id of the session */
                vaccel_id_t id;

                /* id of the remote session */
                vaccel_id_t remote_id;

                /* session-specific resources */
                struct session_resources *resources;

                /* plugin preference */
                unsigned int hint;

                /* backend private data */
                void *priv;

                /* local or virtio option */
                bool is_virtio;
        };

        /* Initialize a new session with the runtime */
        int vaccel_session_init(struct vaccel_session *sess, uint32_t flags);

        /* Update a session with new flags */
        int vaccel_session_update(struct vaccel_session *sess, uint32_t flags);

        /* Tear down a session */
        int vaccel_session_release(struct vaccel_session *sess);

        /* Check if a resource is registered with a session */
        bool vaccel_session_has_resource(const struct vaccel_session *sess,
                                        const struct vaccel_resource *res);

        /* Get resource by id, from registered live resources */
        int vaccel_session_resource_by_id(struct vaccel_session *sess,
                                        struct vaccel_resource **res, vaccel_id_t id);

        /* Get resource by type from live resources.
        * It is required that the resource to be returned, is registered to `sess`
        * session. */
        int vaccel_session_resource_by_type(struct vaccel_session *sess,
                                        struct vaccel_resource **res,
                                        vaccel_resource_type_t type);

        /* Get a list of the registered resources, by type */
        int vaccel_session_resources_by_type(struct vaccel_session *sess,
                                        struct vaccel_resource ***resources,
                                        size_t *nr_found, vaccel_resource_type_t type);
        """
                )

# Resource
ffibuilder.cdef("""
        typedef struct list_entry {
                struct list_entry *next;
                struct list_entry *prev;
        } vaccel_list_entry_t;

        /* Our list type is actually just a normal entry type */
        typedef vaccel_list_entry_t vaccel_list_t;
                
        struct vaccel_resource {
                /* an entry to add this resource in a list */
                vaccel_list_entry_t entry;

                /* resource id */
                vaccel_id_t id;

                /* remote id of the remote resource */
                vaccel_id_t remote_id;

                /* type of the resource */
                vaccel_resource_type_t type;

                /* type of the given path */
                vaccel_path_type_t path_type;

                /* reference counter representing the number of sessions
                * to which this resource is registered to */
                int refcount;

                /* path of the resource. can be an array */
                char **paths;

                /* number of path entities represented by the resource */
                size_t nr_paths;

                /* rundir for this resource if it needs it. can be empty (NULL) */
                char *rundir;

                /* resource representation of the file. can be an array */
                struct vaccel_file **files;

                /* number of file entities represented by the resource */
                size_t nr_files;
        };

        /* Get resource by index from live resources */
        int vaccel_resource_get_by_id(struct vaccel_resource **res, vaccel_id_t id);

        /* Get the first created resource with the given type */
        int vaccel_resource_get_by_type(struct vaccel_resource **res,
                                        vaccel_resource_type_t type);

        /* Get a list of of all created resources with the given type */
        int vaccel_resource_get_all_by_type(struct vaccel_resource ***res,
                                        size_t *nr_found,
                                        vaccel_resource_type_t type);

        /* Get refcount atomically */
        long int vaccel_resource_refcount(const struct vaccel_resource *res);

        /* Initialize resource */
        int vaccel_resource_init(struct vaccel_resource *res, const char *path,
                                vaccel_resource_type_t type);

        /* Initialize resource with multiple file paths */
        int vaccel_resource_init_multi(struct vaccel_resource *res, const char **paths,
                                size_t nr_paths, vaccel_resource_type_t type);

        /* Initialize resource from in-memory data */
        int vaccel_resource_init_from_buf(struct vaccel_resource *res, const void *buf,
                                        size_t nr_bytes, vaccel_resource_type_t type,
                                        const char *filename);

        /* Initialize resource from existing vaccel files */
        int vaccel_resource_init_from_files(struct vaccel_resource *res,
                                        const struct vaccel_file **files,
                                        size_t nr_files,
                                        vaccel_resource_type_t type);

        /* Release resource data */
        int vaccel_resource_release(struct vaccel_resource *res);

        /* Allocate and initialize resource */
        int vaccel_resource_new(struct vaccel_resource **res, const char *path,
                                vaccel_resource_type_t type);

        /* Allocate and initialize resource with multiple file paths */
        int vaccel_resource_multi_new(struct vaccel_resource **res, const char **paths,
                                size_t nr_paths, vaccel_resource_type_t type);

        /* Allocate and initialize resource from in-memory data */
        int vaccel_resource_from_buf(struct vaccel_resource **res, const void *buf,
                                size_t nr_bytes, vaccel_resource_type_t type,
                                const char *filename);

        /* Allocate and initialize resource from existing vaccel files */
        int vaccel_resource_from_files(struct vaccel_resource **res,
                                const struct vaccel_file **files,
                                size_t nr_files, vaccel_resource_type_t type);

        /* Release resource data and free resource created with
        * vaccel_resource_new*() or vaccel_resource_from_*() */
        int vaccel_resource_delete(struct vaccel_resource *res);

        /* Register resource with session */
        int vaccel_resource_register(struct vaccel_resource *res,
                                struct vaccel_session *sess);

        /* Unregister resource from session */
        int vaccel_resource_unregister(struct vaccel_resource *res,
                                struct vaccel_session *sess);

        /* Get directory of a resource created from a directory.
        * If an alloc_path is provided the resulting path string will be allocated and
        * returned there. If not, the path will be copied to out_path.
        * IMPORTANT: If alloc_path == NULL an out_path/out_path_size big enough to
        * hold the resource directory path must be provided */
        int vaccel_resource_directory(struct vaccel_resource *res, char *out_path,
                                size_t out_path_size, char **alloc_path);
        """
                )


# TensorFlow model
# ffibuilder.cdef("""
#         typedef int... vaccel_id_t;
#         struct vaccel_tf_model {
#             struct vaccel_resource *resource;
#             ...;
#         };

#         struct vaccel_tf_saved_model {
#             struct vaccel_resource *resource;
#             ...;
#         };

#         int vaccel_tf_model_new(struct vaccel_tf_model *model, const char *path);
#         int vaccel_tf_model_new_from_buffer(struct vaccel_tf_model *model,
#                         const uint8_t *buff, size_t size);
#         int vaccel_tf_model_destroy(struct vaccel_tf_model *model);
#         int vaccel_tf_saved_model_destroy(struct vaccel_tf_saved_model *model);
#         vaccel_id_t vaccel_tf_model_get_id(const struct vaccel_tf_model *model);
#         """
#                 )

# TensorFlow inference
ffibuilder.cdef("""
        enum vaccel_tf_data_type {
                VACCEL_TF_FLOAT = 1,
                VACCEL_TF_DOUBLE = 2,
                VACCEL_TF_INT32 = 3,  // Int32 tensors are always in 'host' memory.
                VACCEL_TF_UINT8 = 4,
                VACCEL_TF_INT16 = 5,
                VACCEL_TF_INT8 = 6,
                VACCEL_TF_STRING = 7,
                VACCEL_TF_COMPLEX64 = 8,  // Single-precision complex
                VACCEL_TF_COMPLEX = 8,    // Old identifier kept for API backwards compatibility
                VACCEL_TF_INT64 = 9,
                VACCEL_TF_BOOL = 10,
                VACCEL_TF_QINT8 = 11,     // Quantized int8
                VACCEL_TF_QUINT8 = 12,    // Quantized uint8
                VACCEL_TF_QINT32 = 13,    // Quantized int32
                VACCEL_TF_BFLOAT16 = 14,  // Float32 truncated to 16 bits.  Only for cast ops.
                VACCEL_TF_QINT16 = 15,    // Quantized int16
                VACCEL_TF_QUINT16 = 16,   // Quantized uint16
                VACCEL_TF_UINT16 = 17,
                VACCEL_TF_COMPLEX128 = 18,  // Double-precision complex
                VACCEL_TF_HALF = 19,
                VACCEL_TF_RESOURCE = 20,
                VACCEL_TF_VARIANT = 21,
                VACCEL_TF_UINT32 = 22,
                VACCEL_TF_UINT64 = 23,
        };

        struct vaccel_tf_buffer {
                /* data of the buffer */
                void *data;

                /* size of the buffer */
                size_t size;
        };

        struct vaccel_tf_node {
                /* Name of the node */
                char *name;

                /* id of the node */
                int id;
        };

        struct vaccel_tf_tensor {
                /* Tensor's data */
                void *data;

                /* size of the data */
                size_t size;

                /* dimensions of the data */
                int nr_dims;
                int64_t *dims;

                /* Data type */
                enum vaccel_tf_data_type data_type;
                ...;
        };

        struct vaccel_tf_status {
                /* TensorFlow error code */
                uint8_t error_code;

                /* TensorFlow error message */
                char *message;
        };

        /* notfound */
        /*int vaccel_tf_saved_model_set_path(
                struct vaccel_tf_saved_model *model,
                const char *path
                );*/


        int vaccel_tf_session_load(
                struct vaccel_session *session,
                struct vaccel_resource *model,
                struct vaccel_tf_status *status
        );

        // int vaccel_tf_saved_model_register(struct vaccel_tf_saved_model *model);

        int vaccel_tf_session_run(
                struct vaccel_session *session,
                const struct vaccel_resource *model,
                const struct vaccel_tf_buffer *run_options,
                const struct vaccel_tf_node *in_nodes,
                struct vaccel_tf_tensor *const*in, int nr_inputs,
                const struct vaccel_tf_node *out_nodes,
                struct vaccel_tf_tensor **out, int nr_outputs,
                struct vaccel_tf_status *status
        );
                
        int vaccel_tf_session_delete(
                struct vaccel_session *session,
                struct vaccel_resource *model,
                struct vaccel_tf_status *status
        );
        """
                )

# Plugin system
ffibuilder.cdef("""
        struct vaccel_plugin { ...; };
        struct vaccel_op { ...; };

        int vaccel_plugin_register_op(struct vaccel_op *op);
        int vaccel_plugin_register_ops(struct vaccel_op *ops, size_t nr_ops);
        int vaccel_plugin_load(const char *lib);
        int vaccel_plugin_parse_and_load(const char *lib_str);
"""
                )

# Noop API
ffibuilder.cdef("""
        int vaccel_noop(struct vaccel_session *sess);
        """
                )

# Genop API
ffibuilder.cdef("""
        struct vaccel_arg {
                uint32_t argtype;

                uint32_t size;

                void *buf;
        };"""
                )

ffibuilder.cdef("""
        int vaccel_genop(struct vaccel_session *sess, struct vaccel_arg *read,
                        int nr_read, struct vaccel_arg *write, int nr_write);
        """
                )

# Image API
ffibuilder.cdef("""
        int vaccel_image_classification(struct vaccel_session *sess, const void *img,
                        unsigned char *out_text, unsigned char *out_imgname,
                        size_t len_img, size_t len_out_text, size_t len_out_imgname);
        """
                )

ffibuilder.cdef("""
        int vaccel_image_detection(struct vaccel_session *sess, const void *img,
                        unsigned char *out_imgname, size_t len_img,
                        size_t len_out_imgname);
        """
                )

ffibuilder.cdef("""
        int vaccel_image_segmentation(struct vaccel_session *sess, const void *img,
                        unsigned char *out_imgname, size_t len_img,
                        size_t len_out_imgname);
        """
                )

ffibuilder.cdef("""
        int vaccel_image_pose(struct vaccel_session *sess, const void *img,
                        unsigned char *out_imgname, size_t len_img,
                        size_t len_out_imgname);
        """
                )

ffibuilder.cdef("""
        int vaccel_image_depth(struct vaccel_session *sess, const void *img,
                        unsigned char *out_imgname, size_t len_img,
                        size_t len_out_imgname);
        """
                )

#Blas
ffibuilder.cdef("""
        int vaccel_sgemm(struct vaccel_session *sess,
                int64_t m, int64_t n, int64_t k,
                float alpha,
                float *a, int64_t lda,
                float *b, int64_t ldb,
                float beta,
                float *c, int64_t ldc);
        """
                )

#MinMax
ffibuilder.cdef("""
        int vaccel_minmax(struct vaccel_session *sess,
                const double *indata, int ndata,
                int low_threshold, int high_threshold,
                double *outdata,
                double *min, double *max);
        """
                )

#Array copy
# ffibuilder.cdef("""
# int vaccel_fpga_arraycopy(struct vaccel_session *session, int *a, int *b,size_t c);
# """
# )

# #Vector add
# ffibuilder.cdef("""
# int vaccel_fpga_vadd(struct vaccel_session *session, float *a, float *b,
# 	float *c, size_t len_a, size_t len_b);
# """
# )

# #Parallel
# ffibuilder.cdef("""
# int vaccel_fpga_parallel(struct vaccel_session *session, float *a, float *b,
# 	float *add_out, float *mult_out, size_t len_a);
# """
# )

#FPGA
ffibuilder.cdef("""
        int vaccel_fpga_arraycopy(struct vaccel_session *sess, int array[],
                                int out_array[], size_t len_array);

        int vaccel_fpga_mmult(struct vaccel_session *sess, float A[], float B[],
                        float C[], size_t lenA);

        int vaccel_fpga_parallel(struct vaccel_session *sess, float A[], float B[],
                                float add_output[], float mult_output[], size_t len_a);

        int vaccel_fpga_vadd(struct vaccel_session *sess, float A[], float B[],
                        float C[], size_t len_a, size_t len_b);
        """
                )

#Exec API
ffibuilder.cdef("""
        int vaccel_exec(struct vaccel_session *sess, const char *library,
                        const char *fn_symbol, struct vaccel_arg *read,
                        size_t nr_read, struct vaccel_arg *write, size_t nr_write);

        int vaccel_exec_with_resource(struct vaccel_session *sess,
                        struct vaccel_resource *resource,
                        const char *fn_symbol, struct vaccel_arg *read,
                        size_t nr_read, struct vaccel_arg *write,
                        size_t nr_write);
        """
                )

#Exec with resource
ffibuilder.cdef("""
        struct vaccel_file {
                /* name of the file */
                char *name;

                /* Path to file */
                char *path;

                /* Do we own the file? */
                bool path_owned;

                /* Pointer to the contents of the file in case we hold them
                * in a buffer */
                uint8_t *data;
                size_t size;
        };


        int vaccel_file_persist(struct vaccel_file *file, const char *dir,
		        	const char *filename, bool randomize);
        int vaccel_file_init(struct vaccel_file *file, const char *path);
        int vaccel_file_init_from_buf(struct vaccel_file *file, const uint8_t *buf,
		        	    size_t size, const char *filename,
			            const char *dir, bool randomize);
        int vaccel_file_release(struct vaccel_file *file);
        int vaccel_file_new(struct vaccel_file **file, const char *path);
        int vaccel_file_from_buf(struct vaccel_file **file, const uint8_t *buf,
        			 size_t size, const char *filename, const char *dir,
        			 bool randomize);
        int vaccel_file_delete(struct vaccel_file *file);
        bool vaccel_file_initialized(struct vaccel_file *file);
        int vaccel_file_read(struct vaccel_file *file);
        uint8_t *vaccel_file_data(struct vaccel_file *file, size_t *size);
        const char *vaccel_file_path(struct vaccel_file *file);
        """
                )
# struct vaccel_shared_object {
# 	/* Underlying resource object */
# 	struct vaccel_resource *resource;

# 	/* The protobuf file of the shared object */
# 	struct vaccel_file file;

# 	/* Plugin specific data */
# 	void *plugin_data;
# };

# int vaccel_shared_object_new(
# 	struct vaccel_shared_object *object,
# 	const char *path
# );

# int vaccel_shared_object_new_from_buffer(
# 	struct vaccel_shared_object *object,
# 	const uint8_t *buff,
# 	size_t size
# );

# int vaccel_shared_object_destroy(struct vaccel_shared_object *object);

# vaccel_id_t vaccel_shared_object_get_id(
# 	const struct vaccel_shared_object *object
# );

# const uint8_t *vaccel_shared_object_get(
# 	struct vaccel_shared_object *object, size_t *len
# );

#     int vaccel_exec_with_resource(struct vaccel_session *sess, struct vaccel_shared_object *object,
# 		const char *fn_symbol, struct vaccel_arg *read,
# 		size_t nr_read, struct vaccel_arg *write, size_t nr_write);


if __name__ == "__main__":
    ffibuilder.compile(verbose=True)


