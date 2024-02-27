interface ProductsListSearchBarProps {
    handleSearch: (e: React.ChangeEvent<HTMLInputElement>) => void;
    search: string;
}


export default function ProductsListSearchBar({ handleSearch, search }: ProductsListSearchBarProps) {
  return (
    <div className="border-b-2 text-2xl border-black">
      <input
        className="w-full px-2"
        type="text"
        placeholder="Search for items..."
        value={search}
        onChange={handleSearch}
      />
    </div>
  );
}
