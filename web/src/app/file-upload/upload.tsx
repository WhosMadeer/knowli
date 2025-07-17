import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import {
  fileUploadSchema,
  type fileUploadSchemaType,
} from "../../schemas/file-upload";

export function Upload() {
  const form = useForm<fileUploadSchemaType>({
    resolver: zodResolver(fileUploadSchema),
  });

  const onSubmit = async (data: fileUploadSchemaType) => {
    console.log(data);
    const item = data.file.item(0);
    console.log(item);
  };

  return (
    <div>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <input type="file" {...form.register("file")} />
        <button>Test</button>
      </form>
    </div>
  );
}
