/* Copyright 2021, Ableton AG, Berlin. All rights reserved.
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 *  If you would like to incorporate Link into a proprietary software application,
 *  please contact <link-devs@ableton.com>.
 */

#pragma once

#include <processthreadsapi.h>
#include <thread>
#include <utility>

namespace ableton
{
namespace platforms
{
namespace windows
{

struct ThreadFactory
{
  template <typename Callable, typename... Args>
  static std::thread makeThread(std::string name, Callable&& f, Args&&... args)
  {
    return std::thread(
      [](std::string name, Callable&& f, Args&&... args) {
        assert(name.length() < 20);
        wchar_t nativeName[20];
        mbstowcs(nativeName, name.c_str(), name.length() + 1);
        SetThreadDescription(GetCurrentThread(), nativeName);
        f(args...);
      },
      std::move(name), std::forward<Callable>(f), std::forward<Args>(args)...);
  }
};

} // namespace windows
} // namespace platforms
} // namespace ableton
