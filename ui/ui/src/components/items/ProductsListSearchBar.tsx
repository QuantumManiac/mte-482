interface ProductsListSearchBarProps {
    handleSearch: (e: React.ChangeEvent<HTMLInputElement>) => void;
    search: string;
}


export default function ProductsListSearchBar({ handleSearch, search }: ProductsListSearchBarProps) {
  return (
    <div className="border border-black flex-1">
      <input
        type="text"
        placeholder="Search"
        value={search}
        onChange={handleSearch}
      />
    </div>
  );
}
