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

#include <Vrml.hxx>

#include <Standard_Version.hxx>

Standard_OStream& Vrml::VrmlHeaderWriter(Standard_OStream& anOStream)
{
    anOStream << "#VRML V1.0 ascii\n";
    anOStream <<  "\n";
    anOStream << "# Generated by Open CASCADE Technology " << OCC_VERSION_STRING << "\n";
    anOStream <<  "\n";
    return anOStream;
}

Standard_OStream& Vrml::CommentWriter(const Standard_CString  aComment,
			                    Standard_OStream& anOStream) 
{
    anOStream << "# " << aComment << "\n";
    return anOStream;
}
