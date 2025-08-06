import { Button } from "@/components/ui/button";

function App() {
  const values = [0, 1, 2, 3, 4, 5, 6, 7];

  return (
    <div className="flex min-h-svh flex-col items-center justify-center">
      <Button>Click me</Button>

      <div className="grid grid-cols-1 gap-2 w-full">
        {values.map((value) => {
          return <Button key={value}>{value}</Button>;
        })}
      </div>
    </div>
  );
}

export default App;
