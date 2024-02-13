interface ProductsListSearchBarProps {
    handleSearch: (e: React.ChangeEvent<HTMLInputElement>) => void;
    search: string;
}


export default function ProductsListSearchBar({ handleSearch, search }: ProductsListSearchBarProps) {
  return (
    <div className="border-y-2 px-1 text-2xl border-black">
      <input
        className="w-full"
        type="text"
        placeholder="Search for items..."
        value={search}
        onChange={handleSearch}
      />
    </div>
  );
}
