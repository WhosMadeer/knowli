import z from "zod";

export const fileUploadSchema = z.object({
  file: z.instanceof(FileList),
});

export type fileUploadSchemaType = z.infer<typeof fileUploadSchema>;
