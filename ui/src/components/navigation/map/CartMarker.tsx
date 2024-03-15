interface CartMarkerProps {
    x: number;
    y: number;
    heading: number
}

export default function CartMarker({x, y, heading}: CartMarkerProps) {
  const style = {
    transform: `rotate(${heading}deg)`,
    left: `${x}px`,
    top: `${y}px`,
  };

  return (
    <div
      className="absolute flex items-center justify-center"
      style={style} // Applying dynamic styles for rotation and positioning
    >
      <span
        className="text-3xl" // Using Tailwind's text size scale
      >
        ⏫
      </span>
    </div>
  );
}
