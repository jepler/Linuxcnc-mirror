// Created on: 1993-04-07
// Created by: Laurent BUCHARD
// Copyright (c) 1993-1999 Matra Datavision
// Copyright (c) 1999-2014 OPEN CASCADE SAS
//
// This file is part of Open CASCADE Technology software library.
//
// This library is free software; you can redistribute it and/or modify it under
// the terms of the GNU Lesser General Public License version 2.1 as published
// by the Free Software Foundation, with special exception defined in the file
// OCCT_LGPL_EXCEPTION.txt. Consult the file LICENSE_LGPL_21.txt included in OCCT
// distribution for complete text of the license and disclaimer of any warranty.
//
// Alternatively, this file may be used under the terms of Open CASCADE
// commercial license or contractual agreement.


#include <IntCurveSurface_IntersectionSegment.hxx>

IntCurveSurface_IntersectionSegment::IntCurveSurface_IntersectionSegment() 
{ }
//================================================================================
IntCurveSurface_IntersectionSegment::IntCurveSurface_IntersectionSegment(const IntCurveSurface_IntersectionPoint& P1,
									 const IntCurveSurface_IntersectionPoint& P2):
       myP1(P1),myP2(P2)
{ 
} 
//================================================================================
void IntCurveSurface_IntersectionSegment::SetValues(const IntCurveSurface_IntersectionPoint& P1,
						    const IntCurveSurface_IntersectionPoint& P2) { 
  myP1 = P1; 
  myP2 = P2;
} 
//================================================================================
void IntCurveSurface_IntersectionSegment::Values(IntCurveSurface_IntersectionPoint& P1,
						 IntCurveSurface_IntersectionPoint& P2) const
{ 
  P1 = myP1; 
  P2 = myP2;
} 
//================================================================================
void IntCurveSurface_IntersectionSegment::FirstPoint(IntCurveSurface_IntersectionPoint& P1) const { 
  P1 = myP1;
}
//================================================================================
void IntCurveSurface_IntersectionSegment::SecondPoint(IntCurveSurface_IntersectionPoint& P2) const { 
  P2 = myP2;
}
//================================================================================
const IntCurveSurface_IntersectionPoint &
  IntCurveSurface_IntersectionSegment::FirstPoint() const { 
  return(myP1);
}
//================================================================================
const IntCurveSurface_IntersectionPoint &
  IntCurveSurface_IntersectionSegment::SecondPoint() const { 
  return(myP2);
}
//================================================================================
void IntCurveSurface_IntersectionSegment::Dump() const { 
  std::cout<<"\nIntersectionSegment : "<<std::endl;
  myP1.Dump();
  myP2.Dump();
  std::cout<<std::endl;
}

