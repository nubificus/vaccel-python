from cffi import FFI


ffibuilder = FFI()

ffibuilder.set_source(
    "vaccel._vaccel",
    r"""
        #include <session.h>
        #include <tf_model.h>
        #include <ops/tf.h>
        #include <ops/noop.h>
        #include <ops/blas.h>
        #include <ops/minmax.h>
        #include <ops/genop.h>
        #include <ops/image.h>
        #include <resources/tf_saved_model.h>
        #include <resources/shared_object.h>
        #include <plugin.h>
        #include <ops/fpga.h>
        #include <ops/exec.h>
        """,
    libraries=['vaccel-python', 'dl'],
)

# Session API
ffibuilder.cdef("""
        struct vaccel_session {
            uint32_t session_id;
            ...;
        };

        int vaccel_sess_init(struct vaccel_session *sess, uint32_t flags);
        int vaccel_sess_free(struct vaccel_session *sess);
        int vaccel_sess_register(
            struct vaccel_session *sess,
            struct vaccel_resource *resource
        );
        int vaccel_sess_unregister(
            struct vaccel_session *sess,
            struct vaccel_resource *resource
        );
        int vaccel_sess_has_resource(
            struct vaccel_session *sess,
            struct vaccel_resource *resource
        );
        """
                )


# TensorFlow model
ffibuilder.cdef("""
        typedef int... vaccel_id_t;
        struct vaccel_tf_model {
            struct vaccel_resource *resource;
            ...;
        };

        struct vaccel_tf_saved_model {
            struct vaccel_resource *resource;
            ...;
        };

        int vaccel_tf_model_new(struct vaccel_tf_model *model, const char *path);
        int vaccel_tf_model_new_from_buffer(struct vaccel_tf_model *model,
                        const uint8_t *buff, size_t size);
        int vaccel_tf_model_destroy(struct vaccel_tf_model *model);
        int vaccel_tf_saved_model_destroy(struct vaccel_tf_saved_model *model);
        vaccel_id_t vaccel_tf_model_get_id(const struct vaccel_tf_model *model);
        """
                )

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
                int64_t id;
        };

        struct vaccel_tf_tensor {
                /* Tensor's data */
                void *data;

                /* size of the data */
                size_t size;

                /* dimensions of the data */
                int nr_dims;
                int32_t *dims;

                /* Data type */
                enum vaccel_tf_data_type data_type;
                ...;
        };

        struct vaccel_tf_status {
                /* TensorFlow error code */
                uint8_t error_code;

                /* TensorFlow error message */
                const char *message;
        };

        int vaccel_tf_saved_model_set_path(
                struct vaccel_tf_saved_model *model,
                const char *path
                );


        int vaccel_tf_session_load(
                struct vaccel_session *session,
                struct vaccel_tf_saved_model *model,
                struct vaccel_tf_status *status
        );

        int vaccel_tf_saved_model_register(struct vaccel_tf_saved_model *model);

        int vaccel_tf_session_run(
                struct vaccel_session *session,
                const struct vaccel_tf_saved_model *model, const struct vaccel_tf_buffer *run_options,
                const struct vaccel_tf_node *in_nodes, struct vaccel_tf_tensor *const*in, int nr_inputs,
                const struct vaccel_tf_node *out_nodes, struct vaccel_tf_tensor **out, int nr_outputs,
                struct vaccel_tf_status *status
        );
        """
                )

# Plugin system
ffibuilder.cdef("""
        struct vaccel_plugin { ...; };
        struct vaccel_op { ...; };

        int register_plugin(struct vaccel_plugin *plugin);
        int unregister_plugin(struct vaccel_plugin *plugin);
        int register_plugin_function(struct vaccel_op *plugin_op);
        int register_plugin_functions(struct vaccel_op *plugin_ops, size_t nr_ops);
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
                uint32_t size;
                void *buf;
        };"""
                )

ffibuilder.cdef("""
int vaccel_genop(struct vaccel_session *sess, struct vaccel_arg *read,
                int nr_read, struct vaccel_arg *write, int nr_write);"""
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
ffibuilder.cdef("""
int vaccel_fpga_arraycopy(struct vaccel_session *session, int *a, int *b,size_t c);
"""
)

#Vector add
ffibuilder.cdef("""
int vaccel_fpga_vadd(struct vaccel_session *session, float *a, float *b,
	float *c, size_t len_a, size_t len_b);
"""
)

#Parallel
ffibuilder.cdef("""
int vaccel_fpga_parallel(struct vaccel_session *session, float *a, float *b,
	float *add_out, float *mult_out, size_t len_a);
"""
)

#Exec API
ffibuilder.cdef("""
int vaccel_exec(struct vaccel_session *sess, const char *library,
                const char *fn_symbol, struct vaccel_arg *read,
                size_t nr_read, struct vaccel_arg *write, size_t nr_write);
"""
)

#Exec with resource
ffibuilder.cdef("""
struct vaccel_file {
	/* Path to file */
	char *path;

	/* Do we own the file? */
	bool path_owned;

	/* Pointer to the contents of the file in case we hold them
	 * in a buffer */
	uint8_t *data;
	size_t size;
};
struct vaccel_shared_object {
	/* Underlying resource object */
	struct vaccel_resource *resource;

	/* The protobuf file of the shared object */
	struct vaccel_file file;

	/* Plugin specific data */
	void *plugin_data;
};

int vaccel_shared_object_new(
	struct vaccel_shared_object *object,
	const char *path
);

int vaccel_shared_object_new_from_buffer(
	struct vaccel_shared_object *object,
	const uint8_t *buff,
	size_t size
);

int vaccel_shared_object_destroy(struct vaccel_shared_object *object);

vaccel_id_t vaccel_shared_object_get_id(
	const struct vaccel_shared_object *object
);

const uint8_t *vaccel_shared_object_get(
	struct vaccel_shared_object *object, size_t *len
);

    int vaccel_exec_with_resource(struct vaccel_session *sess, struct vaccel_shared_object *object,
		const char *fn_symbol, struct vaccel_arg *read,
		size_t nr_read, struct vaccel_arg *write, size_t nr_write);
"""
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
