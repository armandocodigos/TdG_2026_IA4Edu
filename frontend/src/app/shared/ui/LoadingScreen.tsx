export function LoadingScreen({ message }: { message: string }) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[#f7f4ec] px-6">
      <div className="w-full max-w-sm rounded-3xl border border-[#ddd5c7] bg-white p-8 text-center shadow-sm">
        <div className="mx-auto mb-4 h-12 w-12 animate-pulse rounded-full bg-[#d26d31]/15" />
        <h1 className="text-lg font-semibold text-[#1c180f]">Tesis App</h1>
        <p className="mt-2 text-sm text-[#6f6556]">{message}</p>
      </div>
    </div>
  );
}
