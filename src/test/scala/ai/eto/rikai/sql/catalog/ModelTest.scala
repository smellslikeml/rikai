/*
 * Copyright 2021 Rikai authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package ai.eto.rikai.sql.catalog

import org.scalatest.funsuite.AnyFunSuite

class ModelTest extends AnyFunSuite {

  test("create models") {
    val m = new Model("foo", path = "https://to/foo")
    assert(m.name == "foo")
    assert(m.path == "https://to/foo")
  }

  test("Parsing URLs") {
    val m = Model.fromName("model.//abc").get
    assert(m.name == "abc")

    val httpModel = Model.fromName("model.http://a/b/c/def").get
    assert(httpModel.name == "def")

    val mlflowModel = Model.fromName("model.mlflow://run/1/abc/2").get
    assert(mlflowModel.name == "2")
  }

  test("Parse from local file") {}

  test("Parse from model name") {}
}
