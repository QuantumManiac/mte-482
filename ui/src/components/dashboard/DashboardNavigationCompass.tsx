import Image from "next/image";

interface DashboardNavigationCompassProps {
    heading: number;
    desiredHeading: number | null;
}

export default function DashboardNavigationCompass({heading, desiredHeading}: DashboardNavigationCompassProps) {
  // Calculate the rotation angle for the arrow
  const rotationAngle = (desiredHeading ?? 0) - heading;

    const arrowStyle = {
    transform: `rotate(${rotationAngle}deg)`,
    transition: 'transform 0.5s ease-in-out', // Smooth transition for rotation
  };

  return (
    <div className="flex justify-center items-center h-full w-full relative">
      <div className="absolute" style={arrowStyle}>
        <Image  src="/img/arrow.png" alt="Compass Arrow" width={500} height={500} />
      </div>
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      </div>
    </div>
  );
}
